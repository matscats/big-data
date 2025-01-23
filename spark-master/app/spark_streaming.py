from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, current_timestamp

# Criar sessão Spark com suporte ao Kafka e MongoDB.
spark = (
    SparkSession.builder.appName("MusicStreamingAnalytics")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
    )
    .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/musicdb.analytics")
    .config(
        "spark.mongodb.write.connection.uri",
        f"mongodb://mongodb:27017/musicdb.analytics",
    )
    .getOrCreate()
)

# Configurar leitura do Kafka.
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "musicdb-server.public.music")
    .option("startingOffsets", "earliest")
    .load()
)

schema = """
id INT,
usuario STRING,
nome STRING,
artista STRING,
duracao INT,
genero STRING
"""

music_df = (
    df.selectExpr("CAST(value AS STRING) as json_data")
    .selectExpr(f"from_json(json_data, '{schema}') as data")
    .select("data.*")
    .withColumn("timestamp", to_timestamp(current_timestamp()))
    .withWatermark("timestamp", "10 minutes")
)


genre_stats = music_df.groupBy("genero").count()
user_listening_time = music_df.groupBy("usuario").sum("duracao")
top_artists = music_df.groupBy("artista").count().orderBy("count", ascending=False)


def write_to_mongo(df, epoch_id):
    df.write.format("mongo").mode("append").save()


print(80 * "-")
(
    genre_stats.writeStream.outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
)
(
    user_listening_time.writeStream.outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
)
(
    top_artists.writeStream.outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
)
print(80 * "-")

# genre_stats.writeStream.outputMode("update").foreachBatch(write_to_mongo).start()
# user_listening_time.writeStream.outputMode("update").foreachBatch(write_to_mongo).start()
# top_artists.writeStream.outputMode("complete").foreachBatch(write_to_mongo).start()

spark.streams.awaitAnyTermination()
