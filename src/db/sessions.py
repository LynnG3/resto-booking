"""Database connection and session management.

This module provides core database functionality:
1. Async database engine configuration
2. Session factory for managing database connections
3. Dependency injection for FastAPI database access

The module uses SQLAlchemy's async features to provide non-blocking
database operations throughout the application.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)

from src.core.config import settings

# Создание асинхронного движка для подключения к базе данных
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
)

# Cоздание асинхронной фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session for dependency injection.

    This function is used as a FastAPI dependency to provide database
    sessions to route handlers. It ensures proper connection handling
    and automatic cleanup.

    Yields:
        AsyncSession: A database session that will be automatically
                     closed when the request is complete.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
