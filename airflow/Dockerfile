FROM apache/airflow

# Instalar dependências do provedor MongoDB e OpenLineage
RUN pip install apache-airflow-providers-openlineage apache-airflow-providers-mongo pymongo

# Definir variáveis de ambiente padrão (opcional)
ENV AIRFLOW_HOME=/opt/airflow