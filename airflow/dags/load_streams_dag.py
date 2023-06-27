import os 
import logging 

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.contrib.operators import gcs_to_bq
from airflow.providers.google.cloud.operators.gcs import GCSHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.utils.dates import days_ago # Makes scheduling easy
from airflow.sensors.base import BaseSensorOperator
from google.cloud import storage

import time 

BUCKET = 'music-streams-staging-bucket'
PREFIX = 'files/'

# Define the GCS file sensor class
class GCSFileSensor(BaseSensorOperator):
    def __init__(self, bucket, prefix, **kwargs):
        super().__init__(**kwargs)
        self.bucket = bucket
        self.prefix = prefix
    
    def poke(self, context):
        hook = GoogleCloudStorageHook()
        files = hook.list(self.bucket, prefix=self.prefix)

        file_names = [file for file in files]
        logging.info("files: %s", file_names)
        return False

default_args = {
    'owner': 'Adedotun Adepoju',
    'start_date': days_ago(0),
    'email': ['d.e.adepoju@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

# define the DAG 
dag = DAG(
    dag_id = 'music-streaming-dag',
    default_args=default_args,
    description="DAG to load data streams to BigQuery",
    schedule_interval='30 * * * *' # Minute 30 of every hours
)

# Define the tasks 
gcs_file_sensor_taks = GCSFileSensor(
    task_id="gcs_file_sensor_task",
    bucket= BUCKET,
    prefix=PREFIX,
    mode="poke",
    poke_interval=60,
    timeout= 60*2, # Set timeout to 20 minutes
    soft_fail=True, # Mark as failed if the timeout expires
    dag=dag
)

task1 = BashOperator(
    task_id="log_info",
    bash_command='echo "done"',
    dag=dag
)

gcs_file_sensor_taks >> task1





