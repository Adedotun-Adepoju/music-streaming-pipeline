# music-streaming-pipeline
- [Music Streaming ETL pipeline](#music-streaming-pipeline)
    - [Description](#description)
    - [Architecture](#architecture)
    - [Final Results](#final-results)
    - [Setup](#setup)

## Description
[Eventsim](https://github.com/Interana/eventsim) is a fake streaming service (think of Spotify). It can be used to generate stream events by random users. This project was setup to consume the streaming data being generated by Eventsim. The events are published to Apache Kafka and Apache Spark consumes and processes the data from the Kafka topics. The processed data are then stored in a data lake (GCS) in parquet files. Apache airflow is then used to orchestrate the workflow of writing the files in the data lake to the data warehouse (BigQuery). Google datastudio is then used to visualize metrics from the Dataset. All of the vms are hosted on GCP.

## Architecture 

### Tools
- Cloud provider: Google Cloud Platform 
- Infrastructure as code (IaC): Terraform
- Containerization: Docker 
- Stream Processing - Apache Kafka, Apache Spark (Dataproc)
- Workflow Orchestration - Apache Airflow
- Data Lake: Google Cloud Storage
- Data Warehouse: BigQuery 
- Data Visualization: Google Data Studio

