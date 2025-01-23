FROM bitnami/spark

ENV SPARK_SUBMIT_ARGS="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4"

COPY app/ /opt/spark-apps/

COPY kafka/ /opt/setup_data


RUN tar -xzf /opt/setup_data/kafka.tgz
RUN tar -xzf /opt/setup_data/debezium_postgres.tar.gz
RUN mv kafka_2.12-3.9.0 kafka
RUN mkdir kafka/connect
RUN mv debezium-connector-postgres kafka/connect
ENV KAFKA_HOME=/opt/bitnami/spark/kafka
ENV KAFKA_CLUSTER_ID=I12G-3FmT2C6cH1HptLPBw
RUN echo -e "\nplugin.path=$KAFKA_HOME/connect" >> $KAFKA_HOME/config/connect-standalone.properties
RUN $KAFKA_HOME/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c $KAFKA_HOME/config/kraft/server.properties

#ENV KAFKA_CLUSTER_ID=`"$KAFKA_HOME/bin/kafka-storage.sh random-uuid"`
#CMD ["/opt/bitnami/spark/bin/spark-submit", "/opt/spark-apps/spark_streaming.py"]