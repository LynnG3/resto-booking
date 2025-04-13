# Функция для проверки, занят ли порт
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Функция для поиска свободного порта
find_free_port() {
    local port=8000
    while check_port $port; do
        port=$((port+1))
    done
    echo $port
}

# Остановка всех контейнеров и очистка
cleanup() {
    echo "Stopping all containers..."
    docker stop $(docker ps -a -q) 2>/dev/null || true
    echo "Removing all containers..."
    docker rm $(docker ps -a -q) 2>/dev/null || true
    echo "Cleanup complete!"
}

# Запуск приложения
start_app() {
    local port=$(find_free_port)
    echo "Starting app on port $port..."
    
    # Экспортируем порт для использования в docker-compose
    export APP_PORT=$port
    
    # Запускаем docker-compose с переменной окружения
    docker-compose up --build
}

case "$1" in
    "start")
        start_app
        ;;
    "cleanup")
        cleanup
        ;;
    "restart")
        cleanup
        start_app
        ;;
    *)
        echo "Usage: $0 {start|cleanup|restart}"
        exit 1
        ;;
esac
