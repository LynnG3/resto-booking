"""Настройки конфигурации логгера """
import logging
import sys

from loguru import logger
from pydantic import BaseModel

from src.core.config import settings


class LogConfig(BaseModel):
    """Базовая конфигурация логирования."""
    
    # Форматы логов для разных обработчиков
    CONSOLE_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        "<level>{message}</level>"
    )
    FILE_FORMAT: str = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )

    # Уровень логирования в зависимости от окружения
    LOG_LEVEL: str = "DEBUG" if settings.DEBUG else "INFO"


# Конфигурация логгера
def setup_logging() -> None:
    """Настройка логирования для приложения."""
    # Создаем конфигурацию
    config = LogConfig()
    # Удаляем стандартный обработчик
    logger.remove()
    
    # Добавляем форматированный вывод в консоль
    logger.add(
        sys.stdout,
        format=config.CONSOLE_FORMAT,
        level=config.LOG_LEVEL,
        colorize=True,
        backtrace=True,  # Включаем трейсбек для ошибок
        diagnose=True,   # Добавляем переменные в трейсбек
    )
    
    # Добавляем запись в файл (для продакшена)
    if not settings.DEBUG:
        logger.add(
            "logs/resto_booking.log",
            format=config.FILE_FORMAT,
            level="INFO",
            rotation="1 day",        # Новый файл каждый день
            retention="30 days",     # Храним логи 30 дней
            compression="zip",       # Сжимаем старые логи
            enqueue=True,           # Потокобезопасная запись
        )

    # Перехватываем логи от других библиотек
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(
        logging.StreamHandler(sys.stdout)
    )

    # Логируем запуск с текущими настройками
    logger.info(
        "Logging is configured | Mode: {} | Level: {}",
        "DEBUG" if settings.DEBUG else "PRODUCTION",
        config.LOG_LEVEL,
    )


# Создаем logger для использования в приложении
get_logger = logger.bind(service="resto-booking")
