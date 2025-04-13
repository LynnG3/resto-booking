# resto-booking
A RESTful API for restaurant table reservations built with FastAPI. This project utilizes SQLAlchemy for database interactions. 

## Project structure

.
├── Dockerfile  # Файл для сборки Docker-образа
├── LICENSE
├── README.md
├── scripts  # Служебные скрипты на любой вкус
├── alembic  # Директория для миграций базы данных
│   ├── README
│   ├── env.py  # Конфигурация окружения Alembic
│   ├── script.py.mako  # Шаблон для генерации миграций
│   └── versions  # Директория с версиями миграций
├── alembic.ini  # Конфигурационный файл Alembic
├── docker-compose.yml  # Файл для настройки многоконтейнерного Docker-приложения
├── entrypoint.sh  # Скрипт для запуска приложения в контейнере
├── requirements.txt  # Список зависимостей проекта
├── src
│   ├── __init__.py
│   ├── api  # Директория для API
│   │   ├── __init__.py
│   │   ├── deps
│   │   │   └── __init__.py
│   │   ├── endpoints  # Эндпойнты API
│   │   │   ├── __init__.py
│   │   │   ├── reservations.py
│   │   │   └── tables.py
│   │   └── routers.py
│   ├── core  # Основные компоненты приложения
│   │   ├── __init__.py
│   │   ├── config.py  # Конфигурация приложения
│   │   └── logging.py  # Настройка логирования
│   ├── db
│   │   ├── __init__.py
│   │   ├── database.py  # Логика подключения к базе данных
│   │   └── sessions.py  # Управление сессиями базы данных
│   ├── main.py
│   ├── models  # Модели базы данных
│   │   ├── __init__.py
│   │   ├── reservation.py
│   │   └── table.py
│   ├── schemas  # Pydantic cхемы для валидации данных
│   │   ├── __init__.py
│   │   ├── reservation.py
│   │   └── schemas.py
│   ├── services  # Сервисы бизнес-логики
│   │   ├── __init__.py
│   │   ├── reservation.py
│   │   └── table.py
│   └── utils  # Утилиты и вспомогательные функции
│       ├── __init__.py
│       └── validators.py  # Валидация данных на основе бизнес логики
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_utils
    │   ├── __init__.py
    │   └── test_validators.py
    ├── testcases.txt
    ├── tests_api
    │   ├── __init__.py
    │   ├── test_reservations.py
    │   └── test_tables.py
    └── tests_services
        ├── __init__.py
        ├── test_reservation_service.py
        └── test_table_service.py


## TODO:
- валидация бронирования - нельзя забронить на прошедшую дату
- дополнить скрипты 