import pytest
from fastapi import status
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_reservation(test_client, test_table):
    reservation_data = {
        "customer_name": "John Doe",
        "table_id": test_table.id,
        "reservation_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "duration_minutes": 60
    }
    response = test_client.post("/api/reservations/", json=reservation_data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_get_reservations(test_client):
    response = test_client.get("/api/reservations/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_overlapping_reservation(test_client, test_table, test_reservation):
    # Попытка создать бронь на то же время
    reservation_data = {
        "customer_name": "Jane Doe",
        "table_id": test_table.id,
        "reservation_time": test_reservation.reservation_time.isoformat(),
        "duration_minutes": 60
    }
    response = test_client.post("/api/reservations/", json=reservation_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST