# Workflow Orchestration
- SSH into the vm instance using the command below
```sh
ssh vm-instance
```
- Update the following variables in the .env file in the vm instance
```sh
    GCS_BUCKET = < BUCKET TO LOAD PARQUET FILES FROM >
    BIGQUERY_DATASET = < BIGQUERY DATASET NAME >
    BIGQUERY_TABLE = < BIGQUERY TABLE NAME >
    extra__google_cloud_platform__key_path = <PATH TO SERVICE ACCOUNT JSON FILE>
```

- Start the Airflow server
```sh
docker-compose -f docker-compose-airflow.yaml up -d
```

- Forward port 8080 so you can access it on your local computer. If using Remote-ssh on VS code, go to the ports tab beside the terminal and forward port 9021.

- Try visiting the address http://localhost:8080. The Airflow webserver should open. Use the details below to login
```sh
Username: airflow
password: airflow1
```
The Username and Password can be changed in the .env file by editing these variables `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD`

- Activate the DAG by toggling it on. This DAG will write the parquet files generated to a BigQuery table defined in the .env file. 

- Apache Airflow will run on the 30th minute of every hour and will perform a load job to BigQuery for every parquet file in the bucket loaded within the last hour 

- We will now define eventsim to produce streaming events on a periodic basis to the kafka topic so Spark can consume the streaming data.
```sh
bash eventsim_cron.sh
```
- This adds a CRON job to run the eventsim events producer every 15 minutes. You can modify the bash script to run at any period. The logs of the CRON job will be on the eventsim.log file.

- With this, you can monitor the Apache Airflow DAG from the webserver and monitor the task to load the parquet files to BigQuery. The DAG is scheduled to run on the 30th minute of every hour and load all the parquet data from the previous hour to the Data Warehouse