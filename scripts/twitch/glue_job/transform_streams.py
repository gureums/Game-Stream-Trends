import boto3
import sys
import pytz
import logging
from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, ArrayType
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from pyspark.context import SparkContext
from botocore.exceptions import ClientError

KST = pytz.timezone('Asia/Seoul')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("gureum-twitch-streams-glue-job-logger")

def s3_path_exists(s3_path):
    s3 = boto3.client("s3")
    bucket_name = "gureum-bucket"
    prefix = s3_path.replace(f"s3://{bucket_name}/", "")
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        return "Contents" in response
    except ClientError as e:
        logger.error("Error checking S3 path: %s", str(e))
        return False
    except Exception as e:
        logger.error("Unexpected error in s3_path_exists: %s", str(e))
        return False

try:
    args = getResolvedOptions(sys.argv, ["JOB_NAME", "table_name", "base_output_path"])
except Exception as e:
    logger.error("Error parsing job arguments: %s", str(e))
    raise

try:
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args["JOB_NAME"], args)
except Exception as e:
    logger.error("Error initializing Spark/Glue context or job: %s", str(e))
    raise

try:
    table_name = args["table_name"]
    base_output_path = args["base_output_path"]

    now = datetime.now(KST)
    start_time = now - timedelta(hours=24)
    end_time = now

    json_schema = StructType([
        StructField("data", ArrayType(StructType([
            StructField("id", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("user_login", StringType(), True),
            StructField("user_name", StringType(), True),
            StructField("game_id", StringType(), True),
            StructField("game_name", StringType(), True),
            StructField("type", StringType(), True),
            StructField("title", StringType(), True),
            StructField("tags", ArrayType(StringType()), True),
            StructField("viewer_count", IntegerType(), True),
            StructField("started_at", StringType(), True),
            StructField("language", StringType(), True),
            StructField("thumbnail_url", StringType(), True),
            StructField("tag_ids", ArrayType(StringType()), True),
            StructField("is_mature", BooleanType(), True)
        ])), True),
        StructField("pagination", StructType([
            StructField("cursor", StringType(), True)
        ]), True)
    ])
    
    file_save_count = 0
    
    current_time = start_time
    while current_time < end_time:
        try:
            formatted_date = current_time.strftime("%Y-%m-%d")
            formatted_hour = current_time.strftime("%H")
            raw_data_path = f"s3://gureum-bucket/data/raw/twitch/{table_name}/{formatted_date}/{formatted_hour}/"
            processed_path = f"{base_output_path}/{table_name}/{formatted_date}/{formatted_hour}/"

            if not s3_path_exists(raw_data_path):
                logger.info("Raw data path does not exist, skipping: %s", raw_data_path)
                current_time += timedelta(hours=1)
                continue

            if s3_path_exists(processed_path):
                logger.info("Skipping already processed path: %s", processed_path)
                current_time += timedelta(hours=1)
                continue

            logger.info(f"Processing data from: {raw_data_path}")
            raw_df = spark.read.option("multiline", "true").schema(json_schema).json(raw_data_path)

            processed_df = raw_df.selectExpr("inline(data)").select(
                "id", 
                "user_name", 
                "game_id", 
                "game_name", 
                "type", 
                "title", 
                "viewer_count", 
                "language", 
                "is_mature"
            )

            processed_df.coalesce(1).write.mode("overwrite").parquet(processed_path)
            logger.info(f"Processed data saved to: {processed_path}")
            
            file_save_count += 1
            
        except Exception as e:
            logger.error("Error processing data for date %s and hour %s: %s", formatted_date, formatted_hour, str(e))

        current_time += timedelta(hours=1)
        
    logger.info(f"Total files saved: {file_save_count}")

    try:
        job.commit()
        logger.info("Glue Job completed successfully.")
    except Exception as e:
        logger.error("Error committing Glue Job: %s", str(e))
        raise

except Exception as e:
    logger.error("Unexpected error in Glue Job: %s", str(e))
    raise
