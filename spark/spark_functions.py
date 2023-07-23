from pyspark.sql.functions import from_json, year, month, dayofmonth, hour, col, concat, lit, date_format
from pyspark.sql.types import StringType
import subprocess

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

    spark_df = spark_df.withColumn('timestamp', (spark_df['ts']/1000).cast("timestamp"))

    spark_df = (spark_df
        .withColumn('load_year', year(spark_df["timestamp"]))
        .withColumn('year', year(spark_df["timestamp"]))
        .withColumn('load_month', date_format(spark_df["timestamp"], "MMM"))
        .withColumn('month', month(spark_df["timestamp"]))
        .withColumn('load_day', dayofmonth(spark_df["timestamp"]))
        .withColumn('day', dayofmonth(spark_df["timestamp"]))
        .withColumn('load_hour', hour(spark_df["timestamp"]) + 1)
        .withColumn('hour', hour(spark_df["timestamp"]) + 1)
        .withColumn('full_name', concat(spark_df["firstName"], lit(" "), spark_df["lastName"]))
    )

    spark_df = spark_df.withColumn('timestamp', spark_df['timestamp'].cast(StringType())) # Convert back to string

    spark_df = (spark_df
        .withColumnRenamed("lon", "longitude")
        .withColumnRenamed("lat", "latitude")
    )

    return spark_df