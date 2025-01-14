echo "RODE ISSO UMA ÚNICA VEZ"
docker compose exec postgres sh -c 'echo wal_level = logical >> /var/lib/postgresql/data/postgresql.conf'
echo "AGORA, REINICIE O POSTGRES"