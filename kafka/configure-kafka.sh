#!/bin/bash

# Verifica se o diretório de logs já foi formatado
if [ ! -f /tmp/kraft-combined-logs/meta.properties ]; then
  echo "Formatting storage with a new CLUSTER_ID"
  CLUSTER_ID=$(kafka-storage random-uuid)
  echo "Generated CLUSTER_ID: $CLUSTER_ID"
  kafka-storage format --ignore-formatted --cluster-id $CLUSTER_ID --config /etc/kafka/kraft/server.properties
else
  echo "Storage already formatted. Skipping formatting step."
fi

# Inicia o Kafka
exec /etc/confluent/docker/run
