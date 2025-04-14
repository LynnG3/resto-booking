import pytest
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.reservation import ReservationService
from src.schemas.reservation import ReservationCreate


@pytest.mark.asyncio
async def test_create_reservation(test_db: AsyncSession, test_table):
    """Test reservation creation through service."""
    service = ReservationService(test_db)
    reservation_time = datetime.now() + timedelta(hours=1)
    reservation_data = ReservationCreate(
        customer_name="Service Test Customer",
        table_id=test_table.id,
        reservation_time=reservation_time,
        duration_minutes=60
    )
    reservation = await service.create(reservation_data)
    assert reservation.customer_name == reservation_data.customer_name
    assert reservation.table_id == test_table.id
    assert reservation.duration_minutes == reservation_data.duration_minutes


def check_overlapping_error(exc_info, expected_reservation_id):
    """Проверяет детали ошибки о пересечении бронирований."""
    # Проверяем статус и структуру ошибки
    assert exc_info.value.status_code == 400
    error_detail = exc_info.value.detail
    assert isinstance(error_detail, dict)
    assert error_detail["message"] == "Столик уже занят в этот период времени. "
    assert "existing_reservation" in error_detail

    # Проверяем детали существующей брони
    existing = error_detail["existing_reservation"]
    assert all(key in existing for key in ["id", "start", "end"])
    assert existing["id"] == expected_reservation_id


@pytest.mark.asyncio
async def test_inside_existing_reservation_overlap(test_db: AsyncSession, test_table):
    """Test case: новая бронь внутри существующей."""
    service = ReservationService(test_db)
    base_time = datetime(2025, 5, 1, 12, 0)  # полдень первого мая
    
    # Создаем первую бронь (12:00 - 13:00)
    first_reservation = ReservationCreate(
        customer_name="First Customer",
        table_id=test_table.id,
        reservation_time=base_time,
        duration_minutes=60
    )
    first = await service.create(first_reservation)
    
    # Создаем бронь внутри существующей (12:15 - 12:45)
    overlapping_reservation = ReservationCreate(
        customer_name="Inside Customer",
        table_id=test_table.id,
        reservation_time=base_time + timedelta(minutes=15),
        duration_minutes=30
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create(overlapping_reservation)
    
    check_overlapping_error(exc_info, first.id)


@pytest.mark.asyncio
async def test_starts_during_ends_after_overlap(test_db: AsyncSession, test_table):
    """Test case: новая бронь начинается во время существующей и заканчивается позже."""
    service = ReservationService(test_db)
    base_time = datetime(2025, 5, 1, 12, 0)
    
    # Создаем первую бронь (12:00 - 13:00)
    first_reservation = ReservationCreate(
        customer_name="First Customer",
        table_id=test_table.id,
        reservation_time=base_time,
        duration_minutes=60
    )
    first = await service.create(first_reservation)
    
    # Создаем бронь, начинающуюся во время и заканчивающуюся позже (12:30 - 14:00)
    overlapping_reservation = ReservationCreate(
        customer_name="Overlapping Customer",
        table_id=test_table.id,
        reservation_time=base_time + timedelta(minutes=30),
        duration_minutes=90
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create(overlapping_reservation)
    
    check_overlapping_error(exc_info, first.id)

@pytest.mark.asyncio
async def test_starts_before_ends_during_overlap(test_db: AsyncSession, test_table):
    """Test case: новая бронь начинается раньше и заканчивается во время существующей."""
    service = ReservationService(test_db)
    base_time = datetime(2025, 5, 1, 12, 0)
    
    # Создаем первую бронь (12:00 - 13:00)
    first_reservation = ReservationCreate(
        customer_name="First Customer",
        table_id=test_table.id,
        reservation_time=base_time,
        duration_minutes=60
    )
    first = await service.create(first_reservation)
    
    # Создаем бронь, начинающуюся раньше и заканчивающуюся во время (11:30 - 12:15)
    overlapping_reservation = ReservationCreate(
        customer_name="Overlapping Customer",
        table_id=test_table.id,
        reservation_time=base_time - timedelta(minutes=30),
        duration_minutes=45
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create(overlapping_reservation)
    
    check_overlapping_error(exc_info, first.id)

@pytest.mark.asyncio
async def test_completely_overlaps_existing(test_db: AsyncSession, test_table):
    """Test case: новая бронь полностью перекрывает существующую."""
    service = ReservationService(test_db)
    base_time = datetime(2025, 5, 1, 12, 0)
    
    # Создаем первую бронь (12:00 - 13:00)
    first_reservation = ReservationCreate(
        customer_name="First Customer",
        table_id=test_table.id,
        reservation_time=base_time,
        duration_minutes=60
    )
    first = await service.create(first_reservation)
    
    # Создаем бронь, полностью перекрывающую существующую (11:30 - 13:30)
    overlapping_reservation = ReservationCreate(
        customer_name="Overlapping Customer",
        table_id=test_table.id,
        reservation_time=base_time - timedelta(minutes=30),
        duration_minutes=120
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create(overlapping_reservation)
    
    check_overlapping_error(exc_info, first.id)
