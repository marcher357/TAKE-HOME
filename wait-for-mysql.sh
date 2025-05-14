#!/bin/sh

set -e

echo "⏳ Waiting for MySQL to be ready at $MYSQL_HOST:$MYSQL_PORT..."

while ! nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
  sleep 1
done

echo "✅ MySQL is ready. Starting FastAPI..."

exec "$@"