"""API Endpoints for Repository IQ Engine, summaries, technical debt, recommendations, and benchmark."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.iq import (
    BenchmarkResultSchema,
    ExecutiveSummaryResponse,
    RepositoryIQResponse,
    TechnicalDebtSchema,
    TechnicalSummaryResponse,
)
from app.services.iq_service import IQService
from app.tasks.repository_iq_tasks import repository_iq_task

router = APIRouter()


@router.post(
    "/{id}/iq",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger Repository IQ Analysis",
)
async def trigger_iq_analysis(id: uuid.UUID) -> dict[str, str]:
    """Trigger background Repository IQ Engine calculation."""
    repository_iq_task.delay(str(id))
    return {
        "message": "Repository IQ analysis triggered successfully",
        "repository_id": str(id),
    }


@router.get(
    "/{id}/iq",
    response_model=RepositoryIQResponse,
    summary="Get Overall Repository IQ Report & Score",
)
async def get_iq_report(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve overall Repository IQ score (0-100), maturity level, and subsystem scores."""
    return await IQService.get_iq_report(db, id)


@router.get(
    "/{id}/executive-summary",
    response_model=ExecutiveSummaryResponse,
    summary="Get Executive Summary",
)
async def get_executive_summary(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve Executive Summary report for C-level leadership."""
    return await IQService.get_executive_summary(db, id)


@router.get(
    "/{id}/technical-summary",
    response_model=TechnicalSummaryResponse,
    summary="Get Technical Summary",
)
async def get_technical_summary(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve Technical Summary report for engineering managers and leads."""
    return await IQService.get_technical_summary(db, id)


@router.get(
    "/{id}/strengths",
    response_model=list[str],
    summary="Get Repository Strengths",
)
async def get_strengths(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve identified repository architectural, testing, security, and maintainability strengths."""
    return await IQService.get_strengths(db, id)


@router.get(
    "/{id}/weaknesses",
    response_model=list[str],
    summary="Get Repository Weaknesses",
)
async def get_weaknesses(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve identified repository architectural, testing, security, and maintainability weaknesses."""
    return await IQService.get_weaknesses(db, id)


@router.get(
    "/{id}/technical-debt",
    response_model=TechnicalDebtSchema,
    summary="Get Technical Debt Estimation",
)
async def get_technical_debt(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve estimated technical debt hours, days, and itemized category breakdown."""
    return await IQService.get_technical_debt(db, id)


@router.get(
    "/{id}/recommendations",
    summary="Get Improvement Recommendations",
)
async def get_recommendations(
    id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str | None = Query(None),
    priority: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Retrieve paginated improvement recommendations categorized by timeframe and priority."""
    items, total = await IQService.get_recommendations(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        category=category,
        priority=priority,
    )
    return {
        "items": [
            {
                "id": str(item.id),
                "category": item.category,
                "title": item.title,
                "description": item.description,
                "timeframe": item.timeframe,
                "priority": item.priority,
                "difficulty": item.difficulty,
                "estimated_hours": item.estimated_hours,
            }
            for item in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get(
    "/{id}/benchmark",
    response_model=BenchmarkResultSchema,
    summary="Get Industry Benchmark Percentiles",
)
async def get_benchmark(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve industry benchmarking percentile scores against best practice baselines."""
    return await IQService.get_benchmark(db, id)
