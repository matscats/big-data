from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("KafkaSparkProcessing").getOrCreate()

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "postgres_server.public.table_name")
    .load()
)

# Lógica de transform abaixo.
