from pyspark.sql import SparkSession

# Criar sessão Spark com suporte ao Kafka e MongoDB.
spark = (
    SparkSession.builder.appName("MusicStreamingAnalytics")
    .config("spark.mongodb.output.uri", "mongodb://mongodb/musicdb.analytics")
    .getOrCreate()
)

# Configurar leitura do Kafka.
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "musicdb_server.public.music")
    .option("startingOffsets", "earliest")
    .load()
)

# Transformar dados do Kafka (JSON) em DataFrame estruturado.
schema = """
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
)

# Estatísticas relevantes.
genre_stats = music_df.groupBy("genero").count()
user_listening_time = music_df.groupBy("usuario").sum("duracao")
top_artists = music_df.groupBy("artista").count().orderBy("count", ascending=False)


# Escrever estatísticas no MongoDB.
def write_to_mongo(df, epoch_id):
    df.write.format("mongo").mode("append").save()


genre_stats.writeStream.foreachBatch(write_to_mongo).start()
user_listening_time.writeStream.foreachBatch(write_to_mongo).start()
top_artists.writeStream.foreachBatch(write_to_mongo).start()

spark.streams.awaitAnyTermination()
