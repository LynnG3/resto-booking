import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_get_tables(test_client):
    response = test_client.get("/api/tables/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_table(test_client):
    table_data = {
        "name": "New Table",
        "seats": 4,
        "location": "Main Hall"
    }
    response = test_client.post("/api/tables/", json=table_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == table_data["name"]

@pytest.mark.asyncio
async def test_delete_table(test_client, test_table):
    response = test_client.delete(f"/api/tables/{test_table.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
