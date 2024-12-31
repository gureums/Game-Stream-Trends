# https://api.twitch.tv/helix/streams  # 시청자 많은 순으로 현재 생방송 목록 표시 (최대 100개)
# https://api.twitch.tv/helix/games/top  # 시청자 많은 카테고리 게임 표시


##### Twitch 요청 제한을 보는 방법 (헤더에 포함돼 있음)
# ratelimit_limit = response.headers.get('Ratelimit-Limit')
# ratelimit_remaining = response.headers.get('Ratelimit-Remaining')
# ratelimit_reset = response.headers.get('Ratelimit-Reset')
# print(f"Ratelimit-Limit: {ratelimit_limit}")
# print(f"Ratelimit-Remaining: {ratelimit_remaining}")
# print(f"Ratelimit-Reset: {ratelimit_reset}")

import json
import boto3
import os
import io
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Config:
    TWC_CLIENT_ID = os.getenv('TWC_CLIENT_ID')
    TWC_ACCESS_TOKEN = os.getenv('TWC_ACCESS_TOKEN')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

    @staticmethod
    def get_s3_client():
        # Ensure that boto3 client is returned correctly
        return boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )

    @staticmethod
    def upload_to_s3(data, key):
        try:
            # Convert data to json string and upload to S3
            json_data = json.dumps(data, indent=4)
            buffer = io.BytesIO(json_data.encode('utf-8'))
            # Get the s3 client and upload the data
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
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                s3_key = f"logs/twitch/{self.data_type}/{self.date_str}/fetch_{self.data_type}_{timestamp}.log"
                # Get the s3 client and upload logs
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
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_handler = Config.S3LogHandler(bucket_name, date_str, data_type, buffer_size=buffer_size)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.setLevel(log_level)
        logger.addHandler(log_handler)