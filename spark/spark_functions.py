from pyspark.sql.functions import from_json, year, month, dayofmonth, hour
import subprocess

# def get_last_offsets(checkpointLocation):
#     """
    
#     """
#     # Bash command to get last file in the GCS bucket for storing offsets
#     # bash_command = f"gsutil ls -lh gs://music_streams_spark_jobs/checkpoints/offsets/ | sort -k 2 | tail -n 1"

#     bash_command = f"gsutil ls -lh {checkpointLocation}/offsets/ | sort -k 2 | tail -n 1"

#     process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output, error = process.communicate()

#     # Print the output and errror (if any)
#     print("Command output:", output.decode())
#     print("Command error:", error.decode())

#     file_name = output.split()[-1].decode()
#     print("file_name", file_name)

#     last_line_command = f"gsutil cat {checkpointLocation}/offsets/1 | tail -n 1"
#     print(last_line_command)
#     last_line_process = subprocess.Popen(last_line_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     output, error = last_line_process.communicate()

#     return output.decode()

def process_events(spark, kafka_server, kafka_port, topic, schema, starting_offset="latest"):
    """
    Process specified events from kafka topics

    parameters:
        spark: sparkSession object
        kafka_address: str
            Host address of the kafka bootstrap server 
        topic: str 
            Topic events to process 
        starting_offset: str
    Returns:
        Processed Dataframe
    """

    kafka_stream = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", f"{kafka_server}:{kafka_port}")
        .option("subscribe", topic)
        .option("startingOffsets", starting_offset)
        .load()
    )

    spark_df = (kafka_stream       
        .selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )

    spark_df = (spark_df
        .withColumn('date', (spark_df['ts']/1000).cast("string"))
        .withColumn('year', year(spark_df["timestamp"]))
        .withColumn('month', month(spark_df["timestamp"]))
        .withColumn('day', dayofmonth(spark_df["timestamp"]))
        .withColumn('hour', hour(spark_df["timestamp"]))
        .withColumn('full_name', concat(spark_df["firstName"], lit(" "), df["lastName"]))
    )

    spark_df = (spark_df
        .withColumnRenamed("lon", "longitude")
        .withColumnRenamed("lat", "latitude")
    )

    return spark_df