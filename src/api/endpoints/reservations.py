"""Эндпойты для работы с бронированиями.

Сервисы:
- ReservationService: бизнес-логика для бронирований.
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status

from src.schemas.reservation import ReservationCreate, ReservationResponse
from src.services.reservation import (
    ReservationService, get_reservation_service
)


router = APIRouter()


@router.get(
    '/',
    response_model=List[ReservationResponse],
    status_code=status.HTTP_200_OK,
    summary='Получить список броней',
    description='Возвращает список всех броней с пагинацией'
)
async def get_reservations(
    skip: int = Query(
        default=0,
        ge=0,
        description="Количество пропускаемых записей",
        example=0
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
        description="Максимальное количество записей на странице",
        example=50
    ),
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    return await reservation_service.get_all(skip=skip, limit=limit)


@router.post(
    '/',
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создать бронь',
    description='Создает новую бронь столика'
)
async def create_reservation(
    reservation: ReservationCreate,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    return await reservation_service.create(reservation)


@router.delete(
    '/{reservation_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить бронь',
    description='Удаляет бронь по ее ID'
)
async def delete_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    return await reservation_service.delete(reservation_id)
