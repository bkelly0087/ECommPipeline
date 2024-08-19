from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from data_pipeline.upload_to_snowflake import upload_to_snowflake,get_latest_file,move_file
import os
import sys
sys.path.append('/opt/airflow/data_generation')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 14),
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
generate_data = BashOperator(
    task_id='generate_data',
    bash_command='python /opt/airflow/data_generation/generate_data.py',
    dag=dag,
)

tables = {
    'customers': 'customers',
    'products': 'products',
    'orders': 'orders',
    'order_items': 'order_items'
}

def process_table(table_name):
    latest_file = get_latest_file(table_name)
    if upload_to_snowflake(latest_file, table_name):
        move_file(latest_file)
    else:
        raise Exception(f"Failed to upload {latest_file} to {table_name}")

tables = ['customers', 'products', 'orders', 'order_items']

upload_tasks = []
for table in tables:
    upload_task = PythonOperator(
        task_id=f'upload_{table}',
        python_callable=process_table,
        op_kwargs={'table_name': table},
        dag=dag,
    )
    upload_tasks.append(upload_task)

run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir .',
    dag=dag,
)

generate_data >> upload_tasks >> run_dbt