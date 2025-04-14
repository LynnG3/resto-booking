"""Схемы данных для работы с бронированиями. """
from datetime import datetime
from pydantic import BaseModel, Field


class ReservationBase(BaseModel):
    """Общая схема данных для бронирования."""

    customer_name: str = Field(..., example="Иван Иванов")
    table_id: int = Field(..., ge=1)
    reservation_time: datetime = Field(
        ...,
        example="2025-05-01T14:30:00",
        description="Время бронирования (часы и минуты)"
    )
    duration_minutes: int = Field(..., ge=0, example=120)


class ReservationCreate(ReservationBase):
    """Схема данных для создания брони. """

    pass


class ReservationResponse(ReservationBase):
    """Схема данных для ответа на запрос о брони. """

    id: int

    class Config:
        """Конфигурация для конвертирования ORM-модели в Pydantic-модель. """
        from_attributes = True
