import pytest
from src.services.table import TableService
from src.schemas.table import TableCreate

@pytest.mark.asyncio
async def test_create_table(test_session):
    service = TableService(test_session)
    table_data = TableCreate(
        name="Service Test Table",
        seats=4,
        location="Main Hall"
    )
    table = await service.create_table(table_data)
    assert table.name == table_data.name
    assert table.seats == table_data.seats

@pytest.mark.asyncio
async def test_get_table(test_session, test_table):
    service = TableService(test_session)
    table = await service.get_table(test_table.id)
    assert table is not None
    assert table.id == test_table.id
