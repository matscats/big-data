Ordem:
    1. `docker compose up`;
    1. `sh config_postgres.sh`;
    1. Reinicie o container do Postgres;
    1. `python setup_postgres.py`
    1. `sh setup_kafka.sh`
    1. `sh setup_debezium.sh`
    
Caso já tenha desligado os containers e queira ligá-los de novo sem construí-los do 0, execute novamente o setup_kafka.sh e setup_debezium.sh