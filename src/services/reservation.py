"""Сервис для работы с бронированиями. """
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.db.sessions import get_async_session
from src.core.logging import get_logger
from src.models.table import Table
from src.models.reservation import Reservation
from src.schemas.reservation import ReservationCreate
from src.services.table import TableService, get_table_service
from src.utils.validators import (
    TimeSlot,
    validate_table_available
)


logger = get_logger


class ReservationService:
    """Сервис для работы с бронированиями.

    Args:
        session: Сессия базы данных
        table_service: Экземпляр сервиса столиков
    """
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
        table_service: TableService = Depends(get_table_service)
    ):
        self.session = session
        self.table_service = table_service

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 50
    ) -> List[Reservation]:
        """Получить список всех бронирований."""
        query = (
            select(Reservation)
            .options(joinedload(Reservation.table))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_reservation(self, reservation_id: int) -> Reservation:
        """Получить бронирование по ID или вызвать исключение."""
        reservation = await self.session.get(Reservation, reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Бронь с идентификатором {reservation_id} не найдена.'
            )
        return reservation

    async def create(self, reservation_data: ReservationCreate) -> Reservation:
        """Создать новое бронирование."""
        logger.debug(
            "Creating reservation: table_id={}, time={}",
            reservation_data.table_id,
            reservation_data.reservation_time
        )
        try:
            # 1. Сначала проверяем существование столика
            table = await self.session.get(Table, reservation_data.table_id)
            if not table:
                # Используем стандартную FastAPI ошибку
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Столик с идентификатором {reservation_data.table_id} не найден."
                )
            # Проверяем доступность столика
            await validate_table_available(
                session=self.session,
                table_id=reservation_data.table_id,
                new_slot=TimeSlot(
                    start=reservation_data.reservation_time,
                    duration=reservation_data.duration_minutes
                )
            )
            # Создаем бронирование
            reservation = Reservation(**reservation_data.model_dump())
            self.session.add(reservation)
            await self.session.commit()
            await self.session.refresh(reservation)
            logger.info(
                "Reservation created: id={}, table={}, customer={}",
                reservation.id,
                reservation.table_id,
                reservation.customer_name
            )
            return reservation
        except Exception as e:
            logger.error(
                "Failed to create reservation: {}",
                str(e)
            )
            raise

    async def delete(self, reservation_id: int) -> bool:
        """Удалить бронирование."""
        reservation = await self.get_reservation(reservation_id)
        await self.session.delete(reservation)
        await self.session.commit()
        return True


def get_reservation_service(
    session: AsyncSession = Depends(get_async_session),
    table_service: TableService = Depends(get_table_service)
) -> ReservationService:
    """Получить экземпляр сервиса бронирований
    для использования в зависимостях."""
    return ReservationService(session, table_service)
