import boto3
import sys
import pytz
import logging
from datetime import datetime, timedelta
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from botocore.exceptions import ClientError
from pyspark.sql import Row
from pyspark.sql.functions import to_timestamp, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

KST = pytz.timezone('Asia/Seoul')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("gureum-steam-review-metas-in-use-glue-job-logger")

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

def get_latest_last_modified(s3_path):
    s3 = boto3.client("s3")
    bucket_name = "gureum-bucket"
    prefix = s3_path.replace(f"s3://{bucket_name}/", "")
    
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if "Contents" in response and len(response["Contents"]) > 0:
            latest_modified = max(obj["LastModified"] for obj in response["Contents"])
            return latest_modified
        else:
            logger.info(f"No files found at path: {s3_path}")
            return None
    except ClientError as e:
        logger.error("Error retrieving S3 Last Modified: %s", str(e))
        return None
    except Exception as e:
        logger.error("Unexpected error in get_latest_last_modified: %s", str(e))
        return None

try:
    args = getResolvedOptions(sys.argv, ["JOB_NAME", "table_name", "base_output_path", "base_input_path"])
except Exception as e:
    logger.error("Error parsing job arguments: %s", str(e))
    raise

try:
    from pyspark.context import SparkContext
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
    base_input_path = args["base_input_path"]

    now = datetime.now(KST)
    start_time = now - timedelta(days=1)
    end_time = now
    
    json_schema = StructType([
        StructField("app_id", StringType(), True),
        StructField("review_score", IntegerType(), True),
        StructField("review_score_desc", StringType(), True),
        StructField("total_positive", IntegerType(), True),
        StructField("total_negative", IntegerType(), True),
        StructField("total_reviews", IntegerType(), True),
    ])
    
    file_save_count = 0
    
    timestamp_pattern = r".*_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})\.json"
    current_time = start_time
    while current_time <= end_time:
        try:
            formatted_date = current_time.strftime("%Y-%m-%d")
            raw_data_path = f"{base_input_path}/{table_name}/{formatted_date}/"
            processed_path = f"{base_output_path}/{table_name}/{formatted_date}/"

            if not s3_path_exists(raw_data_path):
                logger.info("Raw data path does not exist, skipping: %s", raw_data_path)
                current_time += timedelta(days=1)
                continue

            if s3_path_exists(processed_path):
                logger.info("Skipping already processed path: %s", processed_path)
                current_time += timedelta(days=1)
                continue

            logger.info(f"Processing data from: {raw_data_path}")
            dynamic_frame = glueContext.create_dynamic_frame.from_options(
                connection_type="s3",
                connection_options={"paths": [raw_data_path]},
                format="json"
            )
            
            last_modified = get_latest_last_modified(raw_data_path)
            if last_modified:
                last_modified_str = last_modified.strftime("%Y-%m-%d-%H-%M-%S")
            else:
                last_modified_str = None

            default_timestamp = (
                last_modified_str if last_modified_str else f"{formatted_date}-00-00-00"
            )
            
            collected_at_value = default_timestamp

            raw_df = dynamic_frame.toDF()
            flattened_rdd = raw_df.rdd.flatMap(lambda row: row.asDict().items()).map(
                lambda x: Row(
                    app_id=x[0],
                    review_score=x[1]['query_summary']['review_score'],
                    review_score_desc=x[1]['query_summary']['review_score_desc'],
                    total_positive=x[1]['query_summary']['total_positive'],
                    total_negative=x[1]['query_summary']['total_negative'],
                    total_reviews=x[1]['query_summary']['total_reviews'],
                )
            )

            flattened_data = spark.createDataFrame(flattened_rdd, schema = json_schema)
            flattened_data = flattened_data.withColumn(
                "collected_at",
                to_timestamp(lit(collected_at_value), "yyyy-MM-dd-HH-mm-ss")
            )

            flattened_data.coalesce(1).write.mode("overwrite").parquet(processed_path)
            logger.info(f"Processed data saved to: {processed_path}")
            
            file_save_count += 1

        except Exception as e:
            logger.error("Error processing data for date %s: %s", formatted_date, str(e))

        current_time += timedelta(days=1)
        
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