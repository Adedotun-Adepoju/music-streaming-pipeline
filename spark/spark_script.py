from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, FloatType
from pyspark.sql.functions import from_json, col
from spark_functions import process_events, get_current_time
from schemas import listen_events_schema, auth_events_schema, page_view_events_schema, status_change_events_schema
import time

spark = (SparkSession
    .builder
    .appName("Eventsim Stream")
    .master(master="yarn")
    .getOrCreate())

spark.streams.resetTerminated()

LISTEN_EVENTS_TOPIC = "listen_events"
AUTH_EVENTS_TOPIC = "auth_events"
PAGE_VIEW_EVENTS_TOPIC = "page_view_events"
STATUS_CHANGE_EVENTS = "status_change_events"

KAFKA_BOOTSTRAP_SERVER = "<EXTERNAL IP ADDRESS OF KAFKA VM INSTANCE>"
KAFKA_PORT = "9092" # Only change this if you made changes in the kafka docker-compose file and terraform main file
GCS_BUCKET = "<ENTER YOUR GCS_BUCKET TO SAVE PROCESSED FILES>"
SPARK_JOBS_BUCKET = "<ENTER YOUR GCS_BUCKET TO SAVE SPARK CONFIGURATION FILES>"

try:
    df_listen_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, KAFKA_PORT, LISTEN_EVENTS_TOPIC, listen_events_schema)

    GCS_STORAGE_PATH = f"gs://{GCS_BUCKET}/files/listen_events"
    GCS_CHECKPOINT_PATH = f"gs://{SPARK_JOBS_BUCKET}/tracking"

    df_listen_events.printSchema()

    print("path",GCS_STORAGE_PATH)

    write_stream_writer = (df_listen_events
        .writeStream
        .format("parquet")
        .partitionBy("load_year", "load_month", "load_day", "load_hour")
        .option("path", GCS_STORAGE_PATH)
        .option("checkpointLocation", GCS_CHECKPOINT_PATH)
        .trigger(processingTime="300 seconds")
        .outputMode("append")
    )

    write_stream_writer.start()

    spark.streams.awaitAnyTermination()
 
except KeyboardInterrupt: 
    write_stream_writer.stop()