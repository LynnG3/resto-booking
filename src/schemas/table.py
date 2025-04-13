"""Схемы данных для работы со столиками. """

from pydantic import BaseModel, Field


class TableBase(BaseModel):
    """Общая схема данных для столика. """

    name: str = Field(..., example="Table 1")
    seats: int = Field(..., ge=1, example=4)
    location: str = Field(..., example="на веранде")


class TableCreate(TableBase):
    """Схема данных для добавления столика. """
    pass


class TableResponse(TableBase):
    """Схема данных ответа на запрос данных столика. """
    id: int

    class Config:
        """Конфигурация для конвертирования ORM-модели в Pydantic-модель. """
        from_attributes = True
