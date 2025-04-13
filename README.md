# 🍽️ Resto-booking

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat&logo=python)](https://www.python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg?style=flat)](https://www.sqlalchemy.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

## 📋 О проекте

RESTful API сервис для управления бронированием столиков в ресторане.
Построен с использованием FastAPI и SQLAlchemy,
предоставляет масштабируемое решение для ресторанного бизнеса. 

### 🚀 Ключевые возможности

- ✨ Управление столиками и их статусами
- 📅 Система бронирования с валидацией
- 🔄 Асинхронная обработка запросов
- 📊 Валидация данных с помощью Pydantic
- 🔍 Подробная документация API (Swagger/ReDoc)

## 🛠 Технологический стек

- **Backend:** FastAPI, Python 3.8+
- **База данных:** PostgreSQL, SQLAlchemy
- **Миграции:** Alembic
- **Валидация:** Pydantic
- **Тестирование:** Pytest
- **Контейнеризация:** Docker, Docker Compose
- **Линтеры и форматтеры:** Black, Flake8, Ruff, MyPy

## Project structure

```
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
```

## TODO:
- валидация бронирования - нельзя забронить на прошедшую дату
- дополнить скрипты 

## 🔍 API Документация

После запуска приложения, документация доступна по следующим URL:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# Запуск тестов с coverage отчетом
pytest --cov=src tests/
```