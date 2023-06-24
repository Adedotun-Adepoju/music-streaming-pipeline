from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, FloatType
from pyspark.sql.functions import from_json, col
from spark_functions import process_events, get_last_offsets
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
KAFKA_BOOTSTRAP_SERVER = "34.79.233.22:9092"

GCS_BUCKET = "music_streams_spark_jobs"

GCS_STORAGE_PATH = f"gs://{GCS_BUCKET}/files"
GCS_CHECKPOINT_PATH = f"gs://{GCS_BUCKET}/checkpoints"

# offset = get_last_offsets(GCS_CHECKPOINT_PATH)
# print(offset)

df_listen_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, LISTEN_EVENTS_TOPIC, listen_events_schema, offset)
# df_auth_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, AUTH_EVENTS_TOPIC, auth_events_schema)
# df_page_view_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, PAGE_VIEW_EVENTS_TOPIC, page_view_events_schema)
# df_status_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, STATUS_CHANGE_EVENTS, status_change_events_schema)

df_listen_events.printSchema()

write_stream_writer = (df_listen_events
    .writeStream
    .format("parquet")
    # .partitionBy("month", "day", "hour")
    .option("path", GCS_STORAGE_PATH)
    .option("checkpointLocation", GCS_CHECKPOINT_PATH)
    .trigger(processingTime="300 seconds")
    .outputMode("append")
)

write_stream_writer.start()

spark.streams.awaitAnyTermination()