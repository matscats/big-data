from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, count, sum, desc
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Configuração do SparkSession com conectores para Kafka e MongoDB
spark = (
    SparkSession.builder.appName("MusicStreamingAnalytics")
    .config(
        "spark.mongodb.output.uri",
        "mongodb://root:password123@mongo:27017/music.analytics",
    )
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
    )
    .getOrCreate()
)

music_schema = StructType(
    [
        StructField("usuario", StringType(), True),
        StructField("nome", StringType(), True),
        StructField("artista", StringType(), True),
        StructField("duracao", IntegerType(), True),
        StructField("genero", StringType(), True),
    ]
)

# Leitura do stream de dados do Kafka
kafka_stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "music_topic")
    .option("startingOffsets", "earliest")
    .load()
)

# Transformação dos dados Kafka para DataFrame estruturado
music_df = (
    kafka_stream.selectExpr("CAST(value AS STRING) as json_data")
    .select(from_json(col("json_data"), music_schema).alias("data"))
    .select("data.*")
)

# Cálculo de estatísticas relevantes
genre_count = music_df.groupBy("genero").count().alias("count")
user_total_duration = music_df.groupBy("usuario").agg(
    sum("duracao").alias("total_duration")
)
top_artists = music_df.groupBy("artista").count().orderBy(desc("count")).limit(5)
top_songs = music_df.groupBy("nome").count().orderBy(desc("count")).limit(5)

# União das estatísticas em um único DataFrame para salvar no MongoDB
statistics_df = (
    genre_count.union(user_total_duration).union(top_artists).union(top_songs)
)

# Escrita contínua no MongoDB
query = (
    statistics_df.writeStream.format("mongodb")
    .outputMode("complete")
    .option("checkpointLocation", "/tmp/checkpoints/music_analytics")
    .start()
)

query.awaitTermination()
