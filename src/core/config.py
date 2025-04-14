"""Общие настройки переменных приложения. """
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки базы данных и приложения."""

    # Настройки базы данных
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/resto-booking"
    )
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    DATABASE_ECHO: bool = False

    # Настройки приложения
    APP_TITLE: str = "Restaurant Booking API"
    APP_DESCRIPTION: str = "API для бронирования столиков в ресторане"
    APP_VERSION: str = "1.0.0"

    model_config = {
        'env_file': '.env',
        'case_sensitive': True,
        'extra': 'allow',
    }


settings = Settings()
