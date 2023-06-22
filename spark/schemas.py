from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType, FloatType, BooleanType

listen_events_schema = (
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

auth_events_schema = (
    StructType()
    .add("ts", StringType())
    .add("sessionId", StringType())
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
    .add("success", StringType())
)

page_view_events_schema = (
    StructType()
    .add("ts", StringType())
    .add("sessionId", StringType())
    .add("page", StringType())
    .add("auth", StringType())
    .add("method", StringType())
    .add("status", IntegerType())
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
    .add("artist", StringType())
    .add("song", StringType())
    .add("duration", FloatType())
)

status_change_events_schema = (
    StructType()
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
    .add("firstName", StringType())
    .add("lastName", StringType())
    .add("gender", StringType())
    .add("registration", StringType())
)