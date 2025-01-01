import os
import json
import boto3
import io
import logging
import pytz
from dotenv import load_dotenv
from datetime import datetime

KST = pytz.timezone('Asia/Seoul')
load_dotenv()

class Config:
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

    @staticmethod
    def get_s3_client():
        return boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )

    @staticmethod
    def download_from_s3(key):
        try:
            S3_BUCKET_NAME = Config.S3_BUCKET_NAME
            logging.info(f"Attempting to download from S3 - Bucket: {S3_BUCKET_NAME}, Key: {key}")
            s3_client = Config.get_s3_client()
            response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
            data = json.loads(response['Body'].read())
            logging.info(f"Successfully downloaded from S3 - Bucket: {S3_BUCKET_NAME}, Key: {key}")
            return data
        except Exception as e:
            logging.error(f"Failed to download from S3 - Bucket: {S3_BUCKET_NAME}, Key: {key}, Error: {e}")

    @staticmethod
    def upload_to_s3(data, key):
        try:
            json_data = json.dumps(data, indent=4)
            buffer = io.BytesIO(json_data.encode('utf-8'))
            s3_client = Config.get_s3_client()
            s3_client.upload_fileobj(buffer, Config.S3_BUCKET_NAME, key)
            logging.info(f"Successfully uploaded data to S3 with key: {key}")
        except Exception as e:
            raise RuntimeError(f"Failed to upload to S3 (key: {key}): {e}")

    # S3 로깅 설정
    class S3LogHandler(logging.Handler):
        def __init__(self, bucket_name, date_str, data_type, buffer_size=10):
            super().__init__()
            self.bucket_name = bucket_name
            self.date_str = date_str
            self.data_type = data_type
            self.buffer_size = buffer_size
            self.log_buffer = io.StringIO()
            self.buffer = []

        def emit(self, record):
            msg = self.format(record)
            self.log_buffer.write(msg + "\n")
            self.buffer.append(record)
            if len(self.buffer) >= self.buffer_size:
                self.flush()

        def flush(self):
            if len(self.buffer) == 0:
                return
            self.log_buffer.seek(0)

            try:
                timestamp = datetime.now(KST).strftime('%Y-%m-%d_%H-%M-%S')
                s3_key = f"logs/steam/{self.data_type}/{self.date_str}/fetch_{self.data_type}_{timestamp}.log"
                s3_client = Config.get_s3_client()
                s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=self.log_buffer.getvalue().encode('utf-8')
                )
                logging.info(f"Logs uploaded to S3: {s3_key}")
            except Exception as e:
                logging.error(f"Failed to upload logs to S3: {e}")

            self.log_buffer = io.StringIO()
            self.buffer = []

    @staticmethod
    def setup_s3_logging(bucket_name, data_type, buffer_size=1000, log_level=logging.INFO):
        date_str = datetime.now(KST).strftime('%Y-%m-%d')
        log_handler = Config.S3LogHandler(bucket_name, date_str, data_type, buffer_size=buffer_size)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.setLevel(log_level)
        logger.addHandler(log_handler)