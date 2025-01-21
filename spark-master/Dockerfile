FROM bitnami/spark

ENV SPARK_SUBMIT_ARGS="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"

COPY app/ /opt/spark-apps/

CMD ["/opt/bitnami/spark/bin/spark-submit", "/opt/spark-apps/spark_streaming.py"]
