"""Repository Comparison REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import (
    RepositoryComparisonRequest,
    RepositoryComparisonResponse,
)
from app.services.comparison_service import ComparisonService

router = APIRouter()


@router.post(
    "/compare",
    response_model=RepositoryComparisonResponse,
    status_code=status.HTTP_200_OK,
)
async def compare_repos(
    req: RepositoryComparisonRequest, db: AsyncSession = Depends(get_db)
) -> Any:
    """Compare scores and metrics across multiple repositories."""
    service = ComparisonService(db)
    return await service.compare_repositories(req)
