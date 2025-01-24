from airflow import DAG
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Função para consultar e exibir os dados do MongoDB
def fetch_and_print_data():
    # Conectar ao MongoDB usando o MongoHook
    hook = MongoHook(mongo_conn_id="mongo_default")
    client = hook.get_conn()
    db = client["testdb"]  # Substitua por seu banco de dados

    # Consultar a coleção "analytics"
    analytics_collection = db["analytics"]
    results = analytics_collection.find()

    # Imprimir os resultados no console
    print("Dados da coleção 'analytics':")
    for doc in results:
        print(doc)


# Definir o DAG com execução a cada 10 segundos
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=5),  # Tempo entre tentativas (caso falhe)
}

with DAG(
    "fetch_mongodb_data",
    default_args=default_args,
    description="Consulta dados do MongoDB e imprime no console",
    schedule_interval=timedelta(seconds=10),  # Executa a cada 10 segundos
    start_date=datetime(2023, 10, 1),  # Data de início do DAG
    catchup=False,  # Não executar execuções passadas
) as dag:

    fetch_data_task = PythonOperator(
        task_id="fetch_and_print_data",
        python_callable=fetch_and_print_data,
    )

    fetch_data_task
