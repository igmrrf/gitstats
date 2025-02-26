#!/bin/sh

echo "Waiting for database to be ready..."
sleep 3 # Ensure DB is up before running migrations (adjust as needed)

# Initialize & Migrate Database
flask db init || true # Avoid error if already initialized
flask db migrate -m "Initial migration"
flask db upgrade

# Start Flask App
exec "$@"
