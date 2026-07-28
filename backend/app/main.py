"""Main FastAPI application factory and entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import health, version
from app.api.v1.router import api_router
from app.core.config.settings import settings
from app.core.logging import setup_logging
from app.exceptions.handlers import register_exception_handlers
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Application lifecycle context manager."""
    setup_logging()
    yield


def create_app() -> FastAPI:
    """FastAPI application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Middleware registration
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(RateLimitMiddleware)
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Exception handlers registration
    register_exception_handlers(app)

    # API Routers registration
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Direct root-level endpoints for GET /health and GET /version
    app.include_router(health.router)
    app.include_router(version.router)

    return app


app = create_app()
