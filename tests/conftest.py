import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from src.main import app
from src.db.base import Base
from src.models.table import Table
from src.models.reservation import Reservation
from src.core.config import settings


TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_resto_booking"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine):
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
async def test_table(test_session):
    table = Table(
        name="Test Table 1",
        seats=4,
        location="Main Hall"
    )
    test_session.add(table)
    await test_session.commit()
    return table

@pytest.fixture
async def test_reservation(test_session, test_table):
    reservation = Reservation(
        customer_name="Test Customer",
        table_id=test_table.id,
        reservation_time=datetime.now() + timedelta(hours=1),
        duration_minutes=60
    )
    test_session.add(reservation)
    await test_session.commit()
    return reservation
