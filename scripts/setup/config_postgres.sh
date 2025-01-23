echo Este comando só deve ser executado uma única vez
docker compose exec postgres sh -c 'echo wal_level = logical >> /var/lib/postgresql/data/postgresql.conf'
echo Reinicie o docker para carregar as alterações