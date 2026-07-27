"""API v1 router composition."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, repositories, version

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(version.router, tags=["Version"])
api_router.include_router(
    repositories.router, prefix="/repositories", tags=["Repositories"]
)
