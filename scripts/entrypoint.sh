#!/bin/bash
echo "Waiting for database..."
while ! pg_isready -h db -p ${DB_PORT} -U ${DB_USER}; do
    sleep 1
done

echo "Database is ready!"

# Применяем миграции (если они есть)
if [ -d "alembic" ]; then
    echo "Running database migrations..."
    alembic upgrade head
fi

# Запускаем приложение
echo "Starting application..."
if [ "$DEBUG" = "True" ]; then
    echo "Running in debug mode..."
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in production mode..."
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000
fi
