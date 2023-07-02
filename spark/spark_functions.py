from pyspark.sql.functions import from_json, year, month, dayofmonth, hour, col, concat, lit, udf
import subprocess

def get_last_offsets(checkpointLocation):
    """
    
    """
    # Bash command to get last file in the GCS bucket for storing offsets
    # bash_command = f"gsutil ls -lh gs://music_streams_spark_jobs/checkpoints/offsets/ | sort -k 2 | tail -n 1"

    # Command to read the last line of the most recent file using the timestamp
    bash_command = f"gsutil ls -lh {checkpointLocation}/offsets/ | sort -k 2 | tail -n 1"

    process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Print the output and errror (if any)
    print("Command output:", output.decode())
    print("Command error:", error.decode())

    file_name = output.split()[-1].decode()
    print("file_name", file_name)

    last_line_command = f"gsutil cat {checkpointLocation}/offsets/{ file_name } | tail -n 1"
    print(last_line_command)
    last_line_process = subprocess.Popen(last_line_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = last_line_process.communicate()

    return output.decode()

# @udf
# def string_decode(s, encoding='utf-8'):
#     if s:
#         return (s.encode('latin1')         # To bytes, required by 'unicode-escape'
#             .decode('unicode-escape') # Perform the actual octal-escaping decode
#             .encode('latin1')         # 1:1 mapping back to bytes
#             .decode(encoding)         # Decode original encoding
#             .strip('\"'))
#     else:
#         return s

def process_events(spark, kafka_server, topic, schema, starting_offset="earliest"):
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

    df = (
        spark.read.format("kafka")
        .option("kafka.bootstrap.servers", kafka_server)
        .option("subscribe", topic)
        .option("startingOffsets", starting_offset)
        .option("endingOffsets", "latest")
        .load()
    )

    df = (df       
        .selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )

    df = df.withColumn('timestamp', (df['ts']/1000).cast("string"))

    df = (df
        .withColumn('year', year(df["timestamp"]))
        .withColumn('month', month(df["timestamp"]))
        .withColumn('day', dayofmonth(df["timestamp"]))
        .withColumn('hour', hour(df["timestamp"]) + 1)
        .withColumn('full_name', concat(df["firstName"], lit(" "), df["lastName"]))
    )

    df = (df
        .withColumnRenamed("lon", "longitude")
        .withColumnRenamed("lat", "latitude")
    )

    return df
