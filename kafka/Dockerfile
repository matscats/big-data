FROM confluentinc/cp-kafka:7.5.0

# Copia o script de configuração para dentro do container
COPY configure-kafka.sh /usr/local/bin/configure-kafka.sh

# Define permissões para o script
USER root
RUN chmod +x /usr/local/bin/configure-kafka.sh


# Substitui o comando padrão para incluir a configuração do CLUSTER_ID
CMD ["/usr/local/bin/configure-kafka.sh"]
