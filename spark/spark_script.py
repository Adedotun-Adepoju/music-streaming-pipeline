from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, FloatType
from pyspark.sql.functions import from_json, col
from spark_functions import process_events, get_last_offsets
from schemas import listen_events_schema, auth_events_schema, page_view_events_schema, status_change_events_schema
import time
import datetime

spark = (SparkSession
    .builder
    .appName("Eventsim Stream")
    .master(master="yarn")
    .getOrCreate())

spark.streams.resetTerminated()

today = datetime.datetime.now()

year = today.strftime('%Y')
month = today.strftime('%h') # abbreviated month
day = today.strftime('%d')
hour = int(today.strftime('%H')) + 1

LISTEN_EVENTS_TOPIC = "listen_events"
AUTH_EVENTS_TOPIC = "auth_events"
PAGE_VIEW_EVENTS_TOPIC = "page_view_events"
STATUS_CHANGE_EVENTS = "status_change_events"
KAFKA_BOOTSTRAP_SERVER = "34.77.183.224:9092"

GCS_BUCKET = "music-streams-staging-bucket"
SPARK_JOBS_BUCKET = "music_streams_spark_jobs"

GCS_STORAGE_PATH = f"gs://{GCS_BUCKET}/files/listen_events/{year}/{month}/{day}/{hour}"
GCS_CHECKPOINT_PATH = f"gs://{SPARK_JOBS_BUCKET}/tracker"

# Get the latest offsets
# offset = get_last_offsets(GCS_CHECKPOINT_PATH)
# print("offset", offset)

df_listen_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, LISTEN_EVENTS_TOPIC, listen_events_schema)

df_listen_events.printSchema()

print("path",GCS_STORAGE_PATH)
# print("file_name", file_name)

writer = (df_listen_events
    .write
    .format("parquet")
    # .partitionBy("month", "day", "hour")
    .option("path", GCS_STORAGE_PATH)
    # .option("checkpointLocation", GCS_CHECKPOINT_PATH)
    # .trigger(processingTime="300 seconds")
    .mode("append")
    .save()
)