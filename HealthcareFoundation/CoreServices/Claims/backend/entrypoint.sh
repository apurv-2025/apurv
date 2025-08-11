#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done
echo "Database is ready!"

# Run database migrations (if using Alembic)
# alembic upgrade head

# Start the application
exec "$@" 