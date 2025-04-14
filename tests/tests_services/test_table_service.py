import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.table import TableService
from src.schemas.table import TableCreate


@pytest.mark.asyncio
async def test_create_table(test_db: AsyncSession):
    """Test table creation through service."""
    service = TableService(test_db)
    table_data = TableCreate(
        name="Service Test Table",
        seats=4,
        location="Main Hall"
    )
    
    # Создаем таблицу и проверяем результат
    table = await service.create(table_data)
    
    # Проверяем созданный столик
    assert table.name == table_data.name
    assert table.seats == table_data.seats
    assert table.location == table_data.location
    assert table.id is not None  # Проверяем что ID был присвоен

    # Проверяем что столик действительно создан в БД
    result = await test_db.get(table.__class__, table.id)
    assert result is not None
    assert result.id == table.id
