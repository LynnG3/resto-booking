"""Сервис для работы со столиками. """
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.sessions import get_async_session
from src.core.logging import get_logger
from src.models.table import Table
from src.schemas.table import TableCreate


logger = get_logger


class TableService:
    """Сервис для работы со столиками.

    Args:
        session: Сессия базы данных.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 50) -> List[Table]:
        """Получить список всех столиков."""
        query = select(Table).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_table(self, table_id: int) -> Table:
        """Получить столик по ID или вызвать исключение."""
        table = await self.session.get(Table, table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Столик с идентификатором {table_id} не найден.'
            )
        return table

    async def create(self, table_data: TableCreate) -> Table:
        """Добавить столик."""
        logger.debug(
            "Creating table: name={}",
            table_data.name
        )
        try:
            table = Table(**table_data.model_dump())
            self.session.add(table)
            await self.session.commit()
            await self.session.refresh(table)
            logger.info(
                "Table created: id={}, name={}",
                table.id,
                table.name
            )
            return table
        except Exception as e:
            logger.error(
                "Failed to create table: {}",
                str(e)
            )
            raise

    async def delete(self, table_id: int) -> bool:
        """Удалить столик."""
        table = await self.get_table(table_id)
        await self.session.delete(table)
        await self.session.commit()
        return True


def get_table_service(
    session: AsyncSession = Depends(get_async_session)
) -> TableService:
    """Получить экземпляр сервиса столиков для ипользования в зависимостях. """
    return TableService(session)
