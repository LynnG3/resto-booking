"""Модели для работы с бронированиями."""
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Reservation(Base):
    """Модель бронирования столика. """

    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    table_id: Mapped[int] = mapped_column(
        ForeignKey("tables.id", ondelete="CASCADE"),
        nullable=False
    )
    reservation_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    table: Mapped["Table"] = relationship(back_populates="reservations")

    def __str__(self) -> str:
        return (
            f"Reservation(customer='{self.customer_name}', "
            f"table_id={self.table_id}, "
            f"time={self.reservation_time}, "
            f"duration={self.duration_minutes} mins)"
        )

    def __repr__(self) -> str:
        return f"<Reservation(id={self.id}, customer='{self.customer_name}')>"
