from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, FloatType
from pyspark.sql.functions import from_json, col
from spark_functions import process_events
from schemas import listen_events_schema, auth_events_schema, page_view_events_schema, status_change_events_schema
import time
from kafka import KafkaConsumer, TopicPartition
# spark = SparkSession.builder.appName("read_test_stream").getOrCreate()

# spark.sparkContext.setLogLevel("ERROR")
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

GCS_STORAGE_PATH = "gs://music_streams_spark_jobs/files"
GCS_CHECKPOINT_PATH = "gs://music_streams_spark_jobs/checkpoints"

df_listen_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, LISTEN_EVENTS_TOPIC, listen_events_schema)
df_auth_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, AUTH_EVENTS_TOPIC, auth_events_schema)
df_page_view_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, PAGE_VIEW_EVENTS_TOPIC, page_view_events_schema)
df_status_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, STATUS_CHANGE_EVENTS, status_change_events_schema)

df_listen_events.printSchema()

# Convert binary value to string. The value is the data we are actually interested in
# deserialized_df = df_listen_events.selectExpr("CAST(value AS STRING)")\
#     .select(from_json(col("value"), listen_events_schema).alias("data"))\
#         .select("data.*")

# query = df_listen_events.writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .start() 

write_stream_writer = (df_listen_events
    .writeStream
    .format("parquet")
    # .partitionBy("month", "day", "hour")
    .option("path", GCS_STORAGE_PATH)
    .option("checkpointLocation", GCS_CHECKPOINT_PATH)
    # .trigger(processingTime="120 seconds")
    .outputMode("append")
)

write_stream_writer.start()

# spark.streams.awaitAnyTermination()