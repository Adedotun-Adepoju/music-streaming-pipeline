# Workflow Orchestration
- SSH into the vm instance using the command below
```sh
ssh vm-instance
```
- Update the following variables in the .env file in the vm instance
```sh
    GCS_BUCKET = <BUCKET TO LOAD PARQUET FILES FROM>
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

- 

