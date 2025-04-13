"""Main application module.

This module initializes the FastAPI application, configures CORS middleware,
and includes API routers. It serves as the entry point for the web application.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.logging import setup_logging, logger
from src.api.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager.

    This context manager handles startup and shutdown
    events for the application.
    It ensures proper setup of logging and cleanup of resources.

    Args:
        app: The FastAPI application instance
    """
    setup_logging()
    logger.info('Application startup')
    yield
    logger.info('Application shutdown')


# Создаем экземпляр приложения
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Подключение роутеров
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to Restaurant Booking API"}
