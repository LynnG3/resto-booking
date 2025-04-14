
from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_reservations(client: AsyncClient):
    """Test successful retrieval of reservations list."""
    response = await client.get("/api/v1/reservations/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_reservation(client: AsyncClient, test_table):
    """Test successful reservation creation."""
    reservation_time = datetime.now() + timedelta(hours=2)
    reservation_data = {
        "customer_name": "John Doe",
        "table_id": test_table.id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 60
    }
    response = await client.post(
        "/api/v1/reservations/",
        json=reservation_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_name"] == reservation_data["customer_name"]
    assert data["table_id"] == reservation_data["table_id"]


@pytest.mark.asyncio
async def test_overlapping_reservation(
    client: AsyncClient,
    test_table,
    test_reservation
):
    """Test overlapping reservation rejection."""
    reservation_data = {
        "customer_name": "Jane Doe",
        "table_id": test_table.id,
        "reservation_time": test_reservation.reservation_time.isoformat(),
        "duration_minutes": 60
    }
    response = await client.post(
        "/api/v1/reservations/",
        json=reservation_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error_data = response.json()
     # Проверяем структуру ответа
    assert "detail" in error_data
    assert "message" in error_data["detail"]
    assert "existing_reservation" in error_data["detail"]
    # Проверяем сообщение об ошибке
    assert error_data["detail"]["message"] == "Столик уже занят в этот период времени. "
    # Проверяем структуру existing_reservation
    existing_reservation = error_data["detail"]["existing_reservation"]
    assert isinstance(existing_reservation, dict)
    assert all(key in existing_reservation for key in ["id", "start", "end"])