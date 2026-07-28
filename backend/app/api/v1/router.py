"""API v1 router composition."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    analysis,
    architecture,
    health,
    maintainability,
    repositories,
    security,
    version,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(version.router, tags=["Version"])
api_router.include_router(
    repositories.router, prefix="/repositories", tags=["Repositories"]
)
api_router.include_router(
    analysis.router, prefix="/repositories", tags=["Static Analysis"]
)
api_router.include_router(
    architecture.router, prefix="/repositories", tags=["Architecture Intelligence"]
)
api_router.include_router(
    security.router, prefix="/repositories", tags=["Security Intelligence (SAST)"]
)
api_router.include_router(
    maintainability.router,
    prefix="/repositories",
    tags=["Maintainability Intelligence"],
)
