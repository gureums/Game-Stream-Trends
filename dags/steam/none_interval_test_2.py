from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os
from datetime import datetime

script_path = os.path.join(os.path.dirname(__file__), '../../scripts/steam')
sys.path.insert(0, script_path)

from fetch_details import main as fetch_details_main
from fetch_news import main as fetch_news_main
from fetch_discounts import main as fetch_discounts_main
from fetch_reviewmetas import main as fetch_reviewmetas_main

task_info = [
    ('fetch_details', fetch_details_main),
    ('fetch_news', fetch_news_main),
    ('fetch_discounts', fetch_discounts_main),
    ('fetch_reviewmetas', fetch_reviewmetas_main)
]

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2024, 12, 20),
}

dag = DAG(
    'test_daily',
    default_args=default_args,
    description='A DAG for triggering Steam data fetch details, news, discounts, review metadata',
    schedule_interval=None,
    catchup=False,
    concurrency=4,
    max_active_runs=4,
)

for task_id, python_callable in task_info:
    PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        retries=default_args['retries'],
        start_date=default_args['start_date'],
        dag=dag,
    )
