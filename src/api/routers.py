"""Роутеры для API.

Сервисы:
- reservations: бизнес-логика для бронирований.
- tables: бизнес-логика для столиков.
"""
from fastapi import APIRouter

from src.api.endpoints import reservations, tables

api_router = APIRouter()

api_router.include_router(
    reservations.router,
    prefix="/reservations",
    tags=["reservations"]
)

api_router.include_router(
    tables.router,
    prefix="/tables",
    tags=["tables"]
)
