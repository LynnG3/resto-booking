# src/utils/validators.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.reservation import Reservation
from src.models.table import Table


async def validate_table_exists(
    table_id: int,
    session: AsyncSession
) -> Optional[Table]:
    """Проверяет существование столика."""
    query = select(Table).where(Table.id == table_id)
    result = await session.execute(query)
    table = result.scalar_one_or_none()

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Столик с иденификатором {table_id} не найден. '
        )
    return table


async def validate_reservation_exists(
    reservation_id: int,
    session: AsyncSession
) -> Optional[Reservation]:
    """Проверяет существование брони."""
    query = select(Reservation).where(Reservation.id == reservation_id)
    result = await session.execute(query)
    reservation = result.scalar_one_or_none()

    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Бронь с идентификатором id {reservation_id} не найдена.'
        )
    return reservation


@dataclass
class TimeSlot:
    """Временной слот для проверки доступности бронирования. """
    start: datetime
    duration: int

    @property
    def end(self) -> datetime:
        """Время окончания бронирования."""
        return self.start + timedelta(minutes=self.duration)

    def overlaps(self, other: 'TimeSlot') -> bool:
        """Проверяет пересечение с другим временным слотом."""
        return (
            self.start < other.end
            and other.start < self.end
        )


async def validate_table_available(
    session: AsyncSession,
    table_id: int,
    new_slot: TimeSlot,
    exclude_reservation_id: Optional[int] = None
) -> bool:
    """
    Проверяет доступность столика на указанное время.

    Args:
        session: Сессия базы данных
        table_id: ID столика
        new_slot: Временной слот для проверки
        exclude_reservation_id: ID брони для исключения из проверки
            (используется при обновлении существующей брони)
    Returns:
        bool: True если столик доступен

    Raises:
        HTTPException: Если столик занят
    """
    # Получаем все брони столика на эту дату
    query = select(Reservation).where(
        Reservation.table_id == table_id,
        Reservation.reservation_time.between(
            new_slot.start,
            new_slot.end
        )
    )

    if exclude_reservation_id:
        query = query.where(Reservation.id != exclude_reservation_id)

    result = await session.execute(query)
    existing_reservations = result.scalars().all()

    # Проверяем пересечения
    for reservation in existing_reservations:
        existing_slot = TimeSlot(
            start=reservation.reservation_time,
            duration=reservation.duration_minutes
        )

        if new_slot.overlaps(existing_slot):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Столик уже занят в этот период времени. ",
                    "existing_reservation": {
                        "id": reservation.id,
                        "start": reservation.reservation_time.isoformat(),
                        "end": existing_slot.end.isoformat(),
                    }
                }
            )

    return True
