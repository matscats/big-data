docker compose exec -d spark-master /opt/bitnami/spark/kafka/bin/kafka-server-start.sh /opt/bitnami/spark/kafka/config/kraft/server.properties
docker compose exec -d spark-master /opt/bitnami/spark/kafka/bin/connect-standalone.sh /opt/bitnami/spark/kafka/config/connect-standalone.properties
echo "Esperando 3 segundos para não ter que chamar outro script pra fazer o curl"
sleep 3
curl -X POST -H "Content-Type: application/json" --data @../debezium/connector.json http://localhost:8083/connectors