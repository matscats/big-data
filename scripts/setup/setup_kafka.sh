BAIXAR_PLUGIN=$1

DEBEZIUM_DL_LINK=https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/2.7.4.Final/debezium-connector-postgres-2.7.4.Final-plugin.tar.gz
PSQL_PLUGIN_PATH=../../kafka/debezium_postgres.tar.gz
FLAG_PATH=/opt/kafka/config/.flag_do_setup_kafka


if ! [ -e "../../scripts/setup/setup_kafka.sh" ]
then
    echo Por favor execute este script a partir da pasta setup, dentro da pasta script do repositório
    exit 1
fi

CONFIGURADO=$(docker compose exec kafka cat $FLAG_PATH)

if [ "$CONFIGURADO" = "1" ]
then
    echo O container do Kafka já rodou esse script ou sacanearam a flag dele
    echo Somente iniciando o Kafka Connect
    docker compose exec -d kafka /opt/kafka/bin/connect-standalone.sh /opt/kafka/config/connect-standalone.properties
    exit 1
fi

if [ -e "$PSQL_PLUGIN_PATH" ]
then
    echo Arquivo encontrado
else
    echo Arquivo não encontrado
    if [ "$BAIXAR_PLUGIN" = "baixar" ]
    then
        echo Começando download do plugin do Debezium 2.7.4 para Postgres
        wget $DEBEZIUM_DL_LINK -O $PSQL_PLUGIN_PATH
    else
        echo "Você deseja que o script baixe o plugin? [y/qualquer outra entrada para não] "
        read BAIXAR_PLUGIN
        if [ "$BAIXAR_PLUGIN" = "y" ]
        then
            echo Começando download do plugin do Debezium 2.7.4 para Postgres
            wget $DEBEZIUM_DL_LINK -O $PSQL_PLUGIN_PATH
        else
            echo Por favor coloque dentro da pasta kafka da raíz deste repositório o plugin do Debezium para PostgreSQL sob o nome "debezium_postgres.tar.gz", ou habilite o download do plugin chamando "sh $0 baixar" ou respondendo "y" à pergunta
            exit 1
        fi
    fi
fi

echo Criando pasta
docker compose exec kafka mkdir /opt/kafka/connect

echo Configurando o Kafka Connect
#a linha abaixo veio de uma batalha com o chatgpt para conseguir passar esse pipe pra dentro do exec https://chatgpt.com/share/6785adec-19fc-8003-a647-420221a7bfd2
docker compose exec kafka sh -c 'echo "plugin.path=/opt/kafka/connect" >> /opt/kafka/config/connect-standalone.properties'
#poderia ter sido só um arquivo pronto por fora e um docker cp? sim
docker cp $PSQL_PLUGIN_PATH kafka:/opt/kafka/connect/

docker compose exec kafka tar -xf /opt/kafka/connect/debezium_postgres.tar.gz -C /opt/kafka/connect

docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic novas-integracoes

docker compose exec kafka sh -c "echo 1 > $FLAG_PATH"

echo Iniciando o Kafka Connect

docker compose exec -d kafka /opt/kafka/bin/connect-standalone.sh /opt/kafka/config/connect-standalone.properties

echo Tudo pronto, siga para o script de setup do Debezium.