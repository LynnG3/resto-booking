"""Database base configuration.

This module provides the base SQLAlchemy configuration and model class.
It includes the declarative base class and common model utilities.
"""

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Автоматически определяет имя таблицы по имени класса."""
        return cls.__name__.lower() + 's'
