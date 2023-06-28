import os 
import logging 

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryDeleteDatasetOperator,
)
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.gcs_list_operator import GoogleCloudStorageListOperator
from airflow.utils.dates import days_ago # Makes scheduling easy
from datetime import datetime, timedelta
import time 

BUCKET = 'music-streams-staging-bucket'
PREFIX = 'files/'

# function to define what is done to each file
def process_file(**context):
    file_names = context['ti'].xcom_pull(task_ids='list_files')
    logging.info(file_names)
    print(file_names)

default_args = {
    'owner': 'Adedotun Adepoju',
    'start_date': days_ago(0),
    'email': ['d.e.adepoju@gmail.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# define the DAG 
dag = DAG(
    dag_id = 'music-streaming-dag',
    default_args=default_args,
    description="DAG to load data streams to BigQuery",
    schedule_interval='30 * * * *' # Minute 30 of every hours
)

# GCS directory to check for files
current_time = datetime.now()
one_hour_ago = current_time - timedelta(hours=1)

year = one_hour_ago.strftime('%Y')
month = one_hour_ago.strftime('%h')
day = one_hour_ago.strftime('%d')
hour = one_hour_ago.strftime('%H')

FILE_DIRECTORY = f"files/listen_events/{ year }/{ month }/{ day }/13/"
logging.info("here")
# Define the tasks 

# List all files in the GCS directory
list_files = GoogleCloudStorageListOperator(
    task_id='list_files',
    bucket= BUCKET,
    prefix= FILE_DIRECTORY,
    delimiter='.parquet',
    dag=dag
)

# Task to process each file
process_files = PythonOperator(
    task_id="process_files",
    python_callable=process_file,
    # op_kwargs={'file_name': '{{ task_instance.xcom_pull(task_ids="list_files")[0] }}'},
    provide_context=True,
    dag=dag
)

task1 = BashOperator(
    task_id="log_info",
    bash_command='echo "done"',
    dag=dag
)

list_files >> process_files >> task1





