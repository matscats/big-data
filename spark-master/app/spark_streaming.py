from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


""" spark = (
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
) """

spark = (
    SparkSession.builder.appName("MusicStreamingAnalytics")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
    )
    .getOrCreate()
)

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "musicdb-server.public.music")
    .option("startingOffsets", "earliest")
    .load()
)

# Definir o schema dos dados do Kafka
schema = StructType(
    [
        StructField(
            "payload",
            StructType(
                [
                    StructField(
                        "after",
                        StructType(
                            [
                                StructField("id", IntegerType(), True),
                                StructField("usuario", StringType(), True),
                                StructField("nome", StringType(), True),
                                StructField("artista", StringType(), True),
                                StructField("duracao", IntegerType(), True),
                                StructField("genero", StringType(), True),
                            ]
                        ),
                        True,
                    )
                ]
            ),
            True,
        )
    ]
)

# Converter os dados do Kafka de binário para JSON e extrair os campos desejados
music_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.payload.after.*")

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
