"""Trend Metrics REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import TrendMetricResponse
from app.services.trend_service import TrendService

router = APIRouter()


@router.get("/repositories/{id}/trends", response_model=list[TrendMetricResponse])
async def get_trends(
    id: str, limit: int = 30, db: AsyncSession = Depends(get_db)
) -> Any:
    """Fetch time-series trend metrics for a repository."""
    service = TrendService(db)
    return await service.get_repository_trends(id, limit)
