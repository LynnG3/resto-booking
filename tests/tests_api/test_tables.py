import pytest
from httpx import AsyncClient

from fastapi import status

from src.models.table import Table


@pytest.mark.asyncio
async def test_get_tables(client: AsyncClient):
    """Test successful retrieval of tables list."""
    response = await client.get("/api/v1/tables/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_table(client: AsyncClient) -> Table:
    """Test successful creating table."""
    table_data = {
        "name": "New Table",
        "seats": 4,
        "location": "Main Hall"
    }
    response = await client.post("/api/v1/tables/", json=table_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == table_data["name"]
    assert data["seats"] == table_data["seats"]
    assert data["location"] == table_data["location"]


@pytest.mark.asyncio
async def test_delete_table(client: AsyncClient, test_table: Table):
    """Тест на удаление столика"""
    # Сохраняем id до удаления
    table_id = test_table.id
    # Удаляем столик одним запросом
    response = await client.delete(f"/api/v1/tables/{table_id}")
    # Проверяем статус
    assert response.status_code == status.HTTP_204_NO_CONTENT
