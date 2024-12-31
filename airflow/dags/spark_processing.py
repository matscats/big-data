from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from datetime import datetime

now = datetime.now()

with DAG(
    dag_id="spark_etl_pipeline",
    schedule_interval="@daily",
    start_date=now,
) as dag:

    run_spark_job = SparkSubmitOperator(
        task_id="run_spark_job",
        application="/opt/spark/spark_processing.py",
        conn_id="spark_default",
    )
