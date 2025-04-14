"""Test configuration and fixtures.

This module provides pytest fixtures and configuration for testing the application.
It includes database setup and other test dependencies.
"""
import asyncio
import os
from datetime import datetime, timedelta
from typing import AsyncGenerator, AsyncIterator, Generator

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import delete
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


from src.main import app
from src.db.base import Base
from src.db.sessions import get_async_session
from src.models.table import Table
from src.models.reservation import Reservation


@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Фикстура event_loop, работающая как в контейнере, так и локально."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    # Отключить проверку исходного кода
    pytest_asyncio = pytest.importorskip("pytest_asyncio")
    old_loop_check = pytest_asyncio.plugin._is_pytest_asyncio_loop
    pytest_asyncio.plugin._is_pytest_asyncio_loop = lambda loop: True
    yield loop
    # Восстановить оригинальную функцию проверки
    pytest_asyncio.plugin._is_pytest_asyncio_loop = old_loop_check
    # Закрыть loop
    if not loop.is_closed():
        loop.close()


@pytest_asyncio.fixture(scope='session')
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create engine and databases for tests."""
    # Get database for docker or for local testing
    is_docker = os.path.exists('/.dockerenv')
    database_url = (
        'postgresql+asyncpg://postgres:postgres@test_db:5432/test_resto_booking'
        if is_docker else
        'postgresql+asyncpg://postgres:postgres@localhost:5432/test_resto_booking'
    )

    test_engine = create_async_engine(
        database_url,
        future=True,
        poolclass=NullPool,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest_asyncio.fixture
async def test_db(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create clean database before each test."""
    TestingSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

    async with TestingSessionLocal() as session:
        try:
            # Очищаем таблицы перед тестом для чистоты
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(delete(table))
            await session.commit()
            
            yield session
        except Exception as e:
            print(f"Ошибка в test_db: {e}")
            raise
        finally:
            try:
                await session.close()
            except Exception:
                # Игнорируем ошибки закрытия соединения
                pass


@pytest.fixture(scope='session')
def test_app() -> Generator[FastAPI, None, None]:
    """Get FastAPI application instance for testing."""
    yield app

@pytest_asyncio.fixture
async def client(
    test_app: FastAPI,
    test_db: AsyncSession,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create a test client for testing."""
    app = test_app

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        try:
            yield test_db
        finally:
            pass
            # await test_db.rollback()

    app.dependency_overrides[get_async_session] = override_get_db
    transport = httpx.ASGITransport(
        app=app,
        raise_app_exceptions=False
    )
    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://testserver',
        follow_redirects=True
    ) as test_client:
        try:
            yield test_client
        finally:
            test_app.dependency_overrides.clear()


@pytest.fixture
async def test_table(test_db: AsyncSession) -> Table:
    """Fixture test table."""
    async with test_db.begin():  # Используем транзакционный контекст
        table = Table(
            name="Test Table 1",
            seats=4,
            location="Main Hall"
        )
        test_db.add(table)
        await test_db.flush()  # Используем flush вместо commit
        await test_db.refresh(table)
        return table


@pytest.fixture
async def test_reservation(test_db: AsyncSession, test_table: Table) -> Reservation:
    """Fixture test reservation."""
    async with test_db.begin():
        reservation = Reservation(
            customer_name="Test Customer",
            table_id=test_table.id,
            reservation_time=datetime.now() + timedelta(hours=1),
            duration_minutes=60
        )
        test_db.add(reservation)
        await test_db.flush()
        await test_db.refresh(reservation)
        return reservation
