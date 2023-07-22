# Spark cluster setup
- SSH into the vm instance using the command below
```sh
ssh vm-instance
```

- Open this file [spark_script.py](https://github.com/Adedotun-Adepoju/music-streaming-pipeline/blob/main/spark/spark_script.py) and change the following variables in the scipt
```sh
 KAFKA_BOOTSTRAP_SERVER = <EXTERNAL IP ADDRESS OF THE VM INSTANCE>
 KAFKA_PORT = <PORT EXPOSED IN THE FIREWALL> Default to 9092
 GCS_BUCKET = <GCS BUCKET TO WRITE THE PARQUET FILES TO>
 SPARK_JOBS_BUCKET = <BUCKET TO STORE SPARK CHECKPOINTS FILES FOR TRACKING MESSAGES THAT HAVE BEEN CONSUMED>
```

- Open this file [submit_dataproc.sh](https://github.com/Adedotun-Adepoju/music-streaming-pipeline/blob/main/spark/submit_dataproc.sh) and edit the jars flag on line 7 to point to the SPARK_JOBS_BUCKET name. This will compress the spark scripts needed for the spark jobs and load it to the specified bucket so the cluster can run the scripts from there

- Start consuming messages from the Kafka topics
```sh 
cd spark 
bash submit_dataproc.sh
```
- Spark will start processing and transforming the messages in micro-batches. The resulting parquet files will then be loaded to the specified GCS bucket. You can confirm this after a few minutes.

- Note that this job will keep on running and listening for new messages from kafka. Whenever a new message comes in, it runs the job as specified in this file [spark_script.py](https://github.com/Adedotun-Adepoju/music-streaming-pipeline/blob/main/spark/spark_script.py). 

- To stop this job, you will need to go dataproc on the Google cloud console, locate your cluster and stop the job running. 