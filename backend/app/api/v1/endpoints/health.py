"""Health, Liveness, and Readiness check endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.dependencies.db import get_db
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check operational status of the service.",
)
async def get_health() -> HealthResponse:
    """Return primary health status."""
    return HealthResponse(status="healthy")


@router.get(
    "/health/live",
    status_code=status.HTTP_200_OK,
    summary="Kubernetes Liveness Probe",
)
async def liveness_probe() -> dict[str, str]:
    """Liveness probe verifying service is running."""
    return {"status": "alive"}


@router.get(
    "/health/ready",
    status_code=status.HTTP_200_OK,
    summary="Kubernetes Readiness Probe",
)
async def readiness_probe(db: AsyncSession = Depends(get_db)) -> Any:
    """Readiness probe inspecting database connection."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return {"status": "unready", "database": f"error: {str(e)}"}
