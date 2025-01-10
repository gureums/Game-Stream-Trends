from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.models import Variable
from datetime import datetime, timedelta

START_DATE = datetime(2025, 1, 9)
END_DATE = datetime(2025, 1, 9)
TABLE_NAME = 'steam_players'
STAGING_TABLE_NAME = f'{TABLE_NAME}_staging'


REDSHIFT_SILVER_SCHEMA = Variable.get('REDSHIFT_SILVER_SCHEMA')
REDSHIFT_IAM_ROLE = Variable.get('REDSHIFT_IAM_ROLE')
S3_SILVER_BASE_PATH = Variable.get('S3_SILVER_BASE_PATH')
S3_BUCKET_NAME = Variable.get('S3_BUCKET_NAME')

default_args = {
    'owner': 'BEOMJUN',
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'start_date': datetime(2024, 12, 20, 15, 0),  # UTC 15시 = KST 00시
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['cbbsjj0314@gmail.com'],
}

def generate_valid_s3_paths():
    s3_hook = S3Hook(aws_conn_id='aws_gureum')
    valid_paths = []
    current_date = START_DATE

    while current_date <= END_DATE:
        for hour in range(24):
            s3_path = f"{S3_SILVER_BASE_PATH}/steam/players/{current_date.strftime('%Y-%m-%d')}/{hour:02d}/"
            objects = s3_hook.list_keys(bucket_name=S3_BUCKET_NAME, prefix=s3_path)
            parquet_files = [obj for obj in objects if obj.endswith('.parquet')] if objects else []
            if parquet_files:
                valid_paths.append(s3_path)
        current_date += timedelta(days=1)
    
    return valid_paths

s3_paths = generate_valid_s3_paths()

with DAG(
    dag_id='silver_to_redshift_v2',
    default_args=default_args,
    description='Load processed silver data into Redshift using SQLExecuteQueryOperator',
    schedule_interval=None,
    catchup=False,
    tags=['steam', 'silver'],
) as dag:

    create_main_table = SQLExecuteQueryOperator(
        task_id='create_main_table',
        conn_id='redshift-gureum',
        sql=f"""
            CREATE TABLE IF NOT EXISTS {REDSHIFT_SILVER_SCHEMA}.{TABLE_NAME} (
                app_id VARCHAR(255),
                player_count BIGINT,
                result BIGINT,
                collected_at TIMESTAMP,
                ingested_at TIMESTAMP DEFAULT NULL,
                deleted_at TIMESTAMP DEFAULT NULL,
                PRIMARY KEY (app_id, collected_at)
            );
        """,
    )

    create_staging_table = SQLExecuteQueryOperator(
        task_id='create_staging_table',
        conn_id='redshift-gureum',
        sql=f"""
            CREATE TABLE IF NOT EXISTS {REDSHIFT_SILVER_SCHEMA}.{STAGING_TABLE_NAME} (
                app_id VARCHAR(255),
                player_count BIGINT,
                result BIGINT,
                collected_at TIMESTAMP
            );
        """,
    )

    for s3_path in s3_paths:
        truncate_staging_table = SQLExecuteQueryOperator(
            task_id=f'truncate_staging_table_{s3_path.split("/")[-2]}_{s3_path.split("/")[-1]}',
            conn_id='redshift-gureum',
            sql=f"TRUNCATE TABLE {REDSHIFT_SILVER_SCHEMA}.{STAGING_TABLE_NAME};"
        )

        copy_to_staging = SQLExecuteQueryOperator(
            task_id=f'copy_to_staging_{s3_path.split("/")[-2]}_{s3_path.split("/")[-1]}',
            conn_id='redshift-gureum',
            sql=f"""
                COPY {REDSHIFT_SILVER_SCHEMA}.{STAGING_TABLE_NAME} (app_id, player_count, result, collected_at)
                FROM 's3://{S3_BUCKET_NAME}/{s3_path}'
                CREDENTIALS 'aws_iam_role={REDSHIFT_IAM_ROLE}'
                FORMAT AS PARQUET;
            """,
        )

        insert_new_data = SQLExecuteQueryOperator(
            task_id=f'insert_new_data_{s3_path.split("/")[-2]}_{s3_path.split("/")[-1]}',
            conn_id='redshift-gureum',
            sql=f"""
                INSERT INTO {REDSHIFT_SILVER_SCHEMA}.{TABLE_NAME} (app_id, player_count, result, collected_at)
                SELECT s.app_id, s.player_count, s.result, s.collected_at
                FROM {REDSHIFT_SILVER_SCHEMA}.{STAGING_TABLE_NAME} s
                LEFT JOIN {REDSHIFT_SILVER_SCHEMA}.{TABLE_NAME} t
                ON s.app_id = t.app_id AND s.collected_at = t.collected_at
                WHERE t.app_id IS NULL;
            """,
        )

        update_ingested_at = SQLExecuteQueryOperator(
            task_id=f'update_ingested_at_{s3_path.split("/")[-2]}_{s3_path.split("/")[-1]}',
            conn_id='redshift-gureum',
            sql=f"""
                UPDATE {REDSHIFT_SILVER_SCHEMA}.{TABLE_NAME}
                SET ingested_at = timezone('Asia/Seoul', current_timestamp)
                WHERE ingested_at IS NULL;
            """,
        )

        create_main_table >> create_staging_table >> truncate_staging_table >> copy_to_staging >> insert_new_data >> update_ingested_at