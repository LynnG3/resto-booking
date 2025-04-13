#!/bin/bash

# Функция для проверки наличия .env файла
check_env_file() {
    if [ ! -f .env ]; then
        echo "Error: .env file not found!"
        exit 1
    fi
}

# Функция для остановки и удаления контейнеров
cleanup() {
    echo "Stopping and removing existing containers..."
    docker-compose down -v
    docker-compose -f docker-compose.test.yml down -v
}

# Функция для сборки и запуска development окружения
start_dev() {
    echo "Starting development environment..."
    docker-compose build --no-cache
    docker-compose up -d
    echo "Development environment is running!"
    echo "Showing logs in real-time (Ctrl+C to stop watching logs)..."
    docker-compose logs -f
}

# Функция для сборки и запуска тестового окружения
start_test() {
    echo "Starting test environment..."
    docker-compose -f docker-compose.test.yml build --no-cache
    docker-compose -f docker-compose.test.yml up -d
    echo "Test environment is running!"
    echo "Showing logs in real-time (Ctrl+C to stop watching logs)..."
    docker-compose -f docker-compose.test.yml logs -f
}

# Основная логика
check_env_file

case "$1" in
    "dev")
        cleanup
        start_dev
        ;;
    "test")
        cleanup
        start_test
        ;;
    "restart-dev")
        docker-compose restart
        docker-compose logs -f
        ;;
    "restart-test")
        docker-compose -f docker-compose.test.yml restart
        docker-compose -f docker-compose.test.yml logs -f
        ;;
    "logs")
        if [ "$2" != "dev" ] && [ "$2" != "test" ]; then
            echo "Usage: $0 logs {dev|test} [follow]"
            exit 1
        fi
        show_logs "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {dev|test|restart-dev|restart-test}"
        echo "For logs: $0 logs {dev|test} [follow]"
        exit 1
        ;;
esac
