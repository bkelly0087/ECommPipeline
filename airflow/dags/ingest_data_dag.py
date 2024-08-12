import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from data_pipeline.upload_to_snowflake import upload_to_snowflake

def get_latest_file(prefix):
    data_dir = 'data_generation/generated_data'
    files = [f for f in os.listdir(data_dir) if f.startswith(prefix) and f.endswith('.csv')]
    if not files:
        raise FileNotFoundError(f"No files found with prefix {prefix}")
    return os.path.join(data_dir, max(files))

def upload_latest_file(file_prefix, table):
    latest_file = get_latest_file(file_prefix)
    upload_to_snowflake(latest_file, table)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecommerce_pipeline',
    default_args=default_args,
    description='Ecommerce data ingestion pipeline',
    schedule_interval=timedelta(days=1),
)

tables = {
    'customers': 'customers',
    'products': 'products',
    'orders': 'orders',
    'order_items': 'order_items'
}

for file_prefix, table in tables.items():
    PythonOperator(
        task_id=f'upload_{table}',
        python_callable=upload_latest_file,
        op_kwargs={'file_prefix': file_prefix, 'table': table},
        dag=dag,
    )