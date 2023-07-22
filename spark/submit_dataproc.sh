#! /bin/bash

gcloud dataproc jobs submit pyspark \
    --cluster=music-streaming-cluster \
    --properties spark.jars.packages=org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
    --region=europe-west1 \
    --jars=gs://<SPARK_JOBS_BUCKET>/spark_job_archive.zip spark_script.py \
    --files=spark_functions.py,schemas.py