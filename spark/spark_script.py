from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, FloatType
from pyspark.sql.functions import from_json, col
from schemas import listen_events_schema, auth_events_schema, page_view_events_schema, status_change_events_schema
from spark_functions import process_events

spark = SparkSession.builder.appName("read_test_stream").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

LISTEN_EVENTS_TOPIC = "listen_events"
AUTH_EVENTS_TOPIC = "auth_events"
PAGE_VIEW_EVENTS_TOPIC = "page_view_events"
STATUS_CHANGE_EVENTS = "status_change_events"
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"

df_listen_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, LISTEN_EVENTS_TOPIC, listen_events_schema)
df_auth_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, AUTH_EVENTS_TOPIC, auth_events_schema)
df_page_view_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, PAGE_VIEW_EVENTS_TOPIC, page_view_events_schema)
df_status_events = process_events(spark, KAFKA_BOOTSTRAP_SERVER, STATUS_CHANGE_EVENTS, status_change_events_schema)

df_listen_events.printSchema()

# Convert binary value to string. The value is the data we are actually interested in
# deserialized_df = df_listen_events.selectExpr("CAST(value AS STRING)")\
#     .select(from_json(col("value"), listen_events_schema).alias("data"))\
#         .select("data.*")

query = df_listen_events.writeStream \
    .format("console") \
    .outputMode("append") \
    .start() \
    .awaitTermination()



