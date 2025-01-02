from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
import sys
import os
from datetime import datetime, timedelta

script_path = os.path.join(os.path.dirname(__file__), '../../scripts/steam')
sys.path.insert(0, script_path)

from fetch_players import main as fetch_players_main

TASK_INFO = [
    ('fetch_players', fetch_players_main)
]

default_args = {
    'owner': 'BEOMJUN',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 12, 20, 15, 0),  # UTC 15시 = KST 00시
    # 'depends_on_past': False,
    # 'email_on_failure': True,
    # 'email': ['cbbsjj0314@gmail.com'],
}

dag = DAG(
    'glue_crawler_test',
    default_args=default_args,
    description='Collecting concurrent player count data for each Steam appid every 4 hours in KST.',
    schedule_interval=None,
    catchup=False,
    concurrency=4,
    max_active_runs=4,
    # tags=['steam', 'bronze', '4-hourly'],
)

tasks = {}
for task_id, python_callable in TASK_INFO:
    tasks[task_id] = PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        retries=default_args['retries'],
        start_date=default_args['start_date'],
        dag=dag,
    )

trigger_glue_crawler = GlueCrawlerOperator(
    task_id='trigger_glue_crawler',
    crawler_name='gureum-glue-crawler',
    aws_conn_id='aws_gureum',
    region_name='ap-northeast-2',
    dag=dag,
)

for task in tasks.values():
    task >> trigger_glue_crawler