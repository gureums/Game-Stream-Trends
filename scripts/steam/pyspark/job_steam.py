import boto3
from pyspark.context import SparkContext
import sys
import pytz
import logging
from datetime import datetime
from pyspark.sql import DataFrame
from pyspark.sql import functions

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

KST = pytz.timezone('Asia/Seoul')

# Glue Context 초기화
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
logger.info("init Glue Context")

# Glue Client 초기화
client = boto3.client('glue', region_name='ap-northeast-2')  # 적절한 리전으로 설정
logger.info("init Glue Client init")

database_name = "gureum-db"
sources = ["steam", "twitch"]
logger.info("defined db_name & sources[]: %s", sources)

def get_table_names_for_source(source):
    if source == "steam":
        return ["news", "discounts", "players", "review_metas", "details"]
    else:
        logger.warning("Unknown source: %s", source)
        return []

# JSON 데이터 평탄화
# struct 타입은 ".*"
# array 타입은 explode()로 펼치기
def flatten_schema(df: DataFrame) -> DataFrame:
    logger.info("Starting flatten_schema")
    
    # 컬럼 이름이 숫자일 경우, 임의의 이름을 지정
    df = df.toDF(*[f"col_{i}" if c.isdigit() else c for i, c in enumerate(df.columns)])
    
    flat_cols = []
    nested_cols = []

    for column_name, column_type in df.dtypes:
        logger.debug("Processing column: %s with type: %s", column_name, column_type)
        if column_type.startswith("struct"):
            nested_cols.append(column_name)
        elif column_type.startswith("array"):
            flat_cols.append(functions.explode(functions.col(column_name)).alias(column_name))
        else:
            flat_cols.append(functions.col(column_name))

    flat_df = df.select(*flat_cols)

    def flatten_nested(df, nested_cols):
        for nested_col in nested_cols:
            nested_df = df.select(functions.col(nested_col + ".*"))
            df = df.drop(nested_col).join(nested_df, how="left")
        return df

    flat_df = flatten_nested(flat_df, nested_cols)

    logger.info("Flatten schema completed.")
    return flat_df

# Job 초기화
logger.info("Job initialization started")
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
logger.info("Job started: %s", args['JOB_NAME'])

logger.info("start processing data")
# 소스별로 테이블을 처리
for source in sources:
    logger.info("Processing source: %s", source)
    table_names = get_table_names_for_source(source)
    
    for table_name in table_names:
        logger.info("Processing table: %s", table_name)

        try:
            # Data Catalog에서 테이블 로드
            logger.info("Loading table %s from Glue Catalog", table_name)
            dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
                database=database_name,
                table_name=table_name,
                transformation_ctx=f"dynamic_frame_{source}_{table_name}"
            )
            logger.info("Loaded table %s from Glue Catalog.", table_name)

            # DynamicFrame을 DataFrame으로 변환
            logger.info("Converting DynamicFrame to DataFrame for table: %s", table_name)
            data_frame = dynamic_frame.toDF()
            logger.info("Converted DynamicFrame to DataFrame for table: %s", table_name)

            # 데이터 평탄화
            flattened_df = flatten_schema(data_frame)
            logger.info("Flattened data schema for table: %s", table_name)

            # 단일 파티션으로 병합 (단일 파일로 저장)
            logger.info("Merging data into a single partition for table: %s", table_name)
            single_partition_df = flattened_df.coalesce(1)
            logger.info("Data merged into a single partition for table: %s", table_name)

            # 출력 경로 설정 (소스별로 경로 지정)
            date_str = datetime.now(KST).strftime('%Y-%m-%d')
            output_path = f"s3://gureum-bucket/data/processed/{source}/{table_name}/{date_str}/"
            logger.info("Saving processed data to: %s", output_path)

            # Parquet 형식으로 저장
            logger.info("Saving data in Parquet format to S3 for table: %s", table_name)
            single_partition_df.write.mode("overwrite").parquet(output_path)
            logger.info("Data successfully saved to S3 in Parquet format for table: %s", table_name)

        except Exception as e:
            logger.error("Error processing table %s: %s", table_name, str(e))
            raise  # 에러가 발생하면 작업을 중단하고 에러를 재발생시킴

# 작업 종료 시 commit 호출
logger.info("Job commit started")
job.commit()
logger.info("Job %s completed successfully.", args['JOB_NAME'])
