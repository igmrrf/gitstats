#!/bin/bash
set -e

# Create a new database and user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER magicusername WITH PASSWORD 'magicpassword';
    CREATE DATABASE magicdatabase;
    GRANT ALL PRIVILEGES ON DATABASE magicdatabase TO magicusername;
EOSQL

# Run additional SQL scripts if any
for f in /docker-entrypoint-initdb.d/*.sql; do
  [ -f "$f" ] && psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$f"
done

echo "PostgreSQL initialization complete."
# psql -h localhost -U magicusername -d magicdatabase
# psql -h localhost -U yourusername -d yourdatabase
