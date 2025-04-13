"""Эндпойты для работы со столиками.

Сервисы:
- TableService: бизнес-логика для столиков.
"""
from typing import List
from fastapi import APIRouter, Depends, Query, status

from src.schemas.table import TableCreate, TableResponse
from src.services.table import TableService, get_table_service


router = APIRouter()


@router.get(
    '/',
    response_model=List[TableResponse],
    status_code=status.HTTP_200_OK,
    summary='Получить список столиков',
    description='Возвращает список всех столиков с пагинацией.'
)
async def get_tables(
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
    table_service: TableService = Depends(get_table_service)
):
    return await table_service.get_all(skip=skip, limit=limit)


@router.post(
    '/',
    response_model=TableResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Добавить столик',
    description='Создает новый объект столика'
)
async def add_table(
    table: TableCreate,
    table_service: TableService = Depends(get_table_service)
):
    return await table_service.create(table)


@router.delete(
    '/{table_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить столик',
    description='Удаляет столик по его ID'
)
async def delete_table(
    table_id: int,
    table_service: TableService = Depends(get_table_service)
):
    return await table_service.delete(table_id)
