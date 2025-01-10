import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.operators.trigger_dagrun import TriggerDagRunOperator

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
    'owner': 'BEOMJUN',
    'retries': 5,
    'retry_delay': timedelta(minutes=10),
    'start_date': datetime(2024, 12, 20, 15, 0),  # UTC 15시 = KST 00시
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['cbbsjj0314@gmail.com'],
}

dag = DAG(
    'steam_bronze_daily',
    default_args=default_args,
    description='Collecting details, news, discounts, and review metadata for each Steam appid every day at midnight in KST.',
    schedule_interval="0 15 * * *",
    catchup=False,
    concurrency=4,
    max_active_runs=1,
    tags=['steam', 'bronze', 'daily'],
)

tasks = []
for task_id, python_callable in task_info:
    task = PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        retries=default_args['retries'],
        start_date=default_args['start_date'],
        dag=dag,
    )
    tasks.append(task)

# trigger_silver_dag = TriggerDagRunOperator(
#     task_id="trigger_steam_silver_daily",
#     trigger_dag_id="steam_silver_daily",
#     dag=dag,
# )

# tasks >> trigger_silver_dag
