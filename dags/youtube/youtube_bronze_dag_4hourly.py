from airflow import DAG
from airflow.operators.python import PythonOperator
#from scripts.youtube import fetch_videos  # 스크립트에서 함수 호출
from datetime import datetime, timedelta
import sys
import os

script_path = os.path.join(os.path.dirname(__file__), '../../scripts/youtube')
sys.path.insert(0, script_path)
from fetch_videos import fetch_youtube_data

default_args = {
    'owner': 'kimhee',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 1, 15, 0),
}

dag = DAG(
    'youtube_bronze_4hourly',
    default_args=default_args,
    description='Fetch YouTube data and save to bronze_json (Bronze Layer)',
    schedule_interval="0 15,19,23,3,7,11 * * *",
    catchup=False,
    tags=['youtube', 'bronze', '4-hourly'],
)

fetch_task = PythonOperator(
    task_id='fetch_youtube_data',
    python_callable=fetch_youtube_data,  # 스크립트의 함수 호출
    dag=dag,
)