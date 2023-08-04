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

BUCKET = os.environ.get("GCS_BUCKET")
DATASET = os.environ.get("BIGQUERY_DATASET")
TABLE = os.environ.get("BIGQUERY_TABLE")
PREFIX = 'files/'

# function to define what is done to each file.
def process_file(**context):
    file_names = context['ti'].xcom_pull(task_ids='list_files')
    logging.info(file_names)

def set_file_directory(**kwargs):
    execution_time = kwargs['execution_date']
    print("time", execution_time)

    year = execution_time.strftime('%Y')
    month = execution_time.strftime('%h')
    day = int(execution_time.strftime('%d'))
    hour = int(execution_time.strftime('%H')) # Check for the previous hour. Remember this is UTC and VM generates WAT

    # GCS directory to check for files
    FILE_DIRECTORY = f"files/listen_events/load_year={ year }/load_month={ month }/load_day={ day }/load_hour={ hour }/"
    SOURCE_OBJECT_PARAM = f"{FILE_DIRECTORY}*.parquet"

    print("directory", FILE_DIRECTORY)

    kwargs['ti'].xcom_push(key='file_directory', value=FILE_DIRECTORY)
    kwargs['ti'].xcom_push(key='source_object_param', value=SOURCE_OBJECT_PARAM)

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
    schedule_interval='30 * * * *', # Minute 30 of every hours
    catchup=False,
)

# Define the tasks 

# Task to get the file directoru file
set_file_directory = PythonOperator(
    task_id="set_file_directory",
    python_callable=set_file_directory,
    dag=dag
)

# List all files in the GCS directory
list_files = GoogleCloudStorageListOperator(
    task_id='list_files',
    bucket= BUCKET,
    prefix= '{{ ti.xcom_pull(task_ids="set_file_directory", key="file_directory") }}',
    delimiter='.parquet',
    dag=dag
)

# Task to process each file
process_files = PythonOperator(
    task_id="process_files",
    python_callable=process_file,
    provide_context=True, # context to fetch xcoms from the previous task
    dag=dag
)

# Load files to BigQuery 
load_files = GCSToBigQueryOperator(
    task_id = "gcs_to_big_query",
    bucket = BUCKET,
    source_objects=['{{ ti.xcom_pull(task_ids="set_file_directory", key="source_object_param") }}'],
    destination_project_dataset_table=f"{ DATASET }.{ TABLE }",
    source_format='PARQUET',
    autodetect=True,
    schema_fields = [
        {'name': 'userId', 'type': 'INTEGER'},
        {'name': 'song', 'type': 'STRING'},
        {'name': 'artist', 'type': 'STRING'},
        {'name': 'duration', 'type': 'FLOAT'},
        {'name': 'timestamp', 'type': 'STRING'},
        {'name': 'gender', 'type': 'STRING'},
        {'name': 'auth', 'type': 'STRING'},
        {'name': 'state', 'type': 'STRING'},
        {'name': 'city', 'type': 'STRING'},
        {'name': 'full_name', 'type': 'STRING'},
        {'name': 'year', 'type': 'INTEGER'},
        {'name': 'month', 'type': 'INTEGER'},
        {'name': 'day', 'type': 'INTEGER'},
        {'name': 'hour', 'type': 'INTEGER'},
    ],
    write_disposition='WRITE_APPEND',
    dag=dag
)

set_file_directory >> list_files >> process_files >> load_files





