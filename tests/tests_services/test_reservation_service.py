import pytest
from datetime import datetime, timedelta
from src.services.reservation import ReservationService
from src.schemas.reservation import ReservationCreate
from src.utils.validators import TimeSlot
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_reservation(test_session: AsyncSession, test_table):
    service = ReservationService(test_session)
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

@pytest.mark.asyncio
async def test_overlapping_reservations(test_session: AsyncSession, test_table):
    service = ReservationService(test_session)
    base_time = datetime.now() + timedelta(hours=1)

    # Создаем первую бронь
    first_reservation = ReservationCreate(
        customer_name="First Customer",
        table_id=test_table.id,
        reservation_time=base_time,
        duration_minutes=60
    )
    await service.create(first_reservation)

    # Пытаемся создать вторую бронь на то же время
    second_reservation = ReservationCreate(
        customer_name="Second Customer",
        table_id=test_table.id,
        reservation_time=base_time + timedelta(minutes=30),
        duration_minutes=60
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create(second_reservation)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_get_reservation(test_session: AsyncSession, test_reservation):
    service = ReservationService(test_session)
    reservation = await service.get(test_reservation.id)
    assert reservation is not None
    assert reservation.id == test_reservation.id
