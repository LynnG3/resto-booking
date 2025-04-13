"""Модели для работы со столиками"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Table(Base):
    """Модель столика. """
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    seats: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String(255))
    reservations: Mapped[list['Reservation']] = relationship(
        "Reservation",
        back_populates="table",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __str__(self) -> str:
        return (
            f"Table(id={self.id}, name='{self.name}', "
            f"seats={self.seats}, location='{self.location}')"
        )

    def __repr__(self) -> str:
        return f"<Table(id={self.id}, name='{self.name}')>"
