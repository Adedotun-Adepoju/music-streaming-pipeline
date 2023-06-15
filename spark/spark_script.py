from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, FloatType
from pyspark.sql.functions import from_json, col


# sc = SparkContext.getOrCreate(SparkConf().setMaster("spark://localhost:7077"))

# sc.setLogLevel("ERROR")

# spark = SparkSession.builder.getOrCreate()

# spark = (
#     SparkSession.builder.appName("Kafka Pyspark Streaming").master("spark://localhost:7077").getOrCreate()
# )

spark = SparkSession.builder.appName("read_test_straeam").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

KAFKA_TOPIC_NAME = "listen_events"
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
    .option("subscribe", KAFKA_TOPIC_NAME)
    .option("startingOffsets", "latest")
    .load()  
)

df.printSchema()

# Convert binary value to string. The value is the data we are actually interested in
# base_df = df.selectExpr("CAST(value AS STRING)")

# Convert JSON String to Data Frame columns using custom schema 

listen_event_schema = (
    StructType()
    .add("artist", StringType())
    .add("song", StringType())
    .add("duration", FloatType())
    .add("ts", StringType())
    .add("sessionId", StringType())
    .add("auth", StringType())
    .add("level", StringType())
    .add("itemInSession", IntegerType())
    .add("city", StringType())
    .add("zip", StringType())
    .add("state", StringType())
    .add("userAgent", StringType())
    .add("lon", FloatType())
    .add("lat", FloatType())
    .add("userId", IntegerType())
    .add("lastName", StringType())
    .add("firstName", StringType())  
    .add("gender", StringType())
    .add("registration", StringType())
)

# listen_dataframe = base_df.select(from_json(col("value"), listen_event_schema).alias("data")).select("data.*")


# query = listen_dataframe.writeStream \
#     .format("console") \
#     .start()

# query.awaitTermination()

deserialized_df = df.selectExpr("CAST(value AS STRING)") \
.select(from_json(col("value"), listen_event_schema).alias("data")) \
.select("data.*")

query = deserialized_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start() \
    .awaitTermination()



