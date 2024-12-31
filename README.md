Executar:

**Levantar os containers**
```
$ docker-compose up -d
```

**Configurar o conector PostgreSQL**
```
curl -X POST -H "Content-Type: application/json" \
    --data @kafka/debezium-connector-postgres.json \
    http://localhost:8083/connectors
```

**Configurar o conector MongoDB**
```
curl -X POST -H "Content-Type: application/json" \
    --data @kafka/debezium-connector-mongo.json \
    http://localhost:8083/connectors
```