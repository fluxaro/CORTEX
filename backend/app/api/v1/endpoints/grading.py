"""API Endpoints for CORTEX Repository Grade Reports, AI summaries, debt, persona views, and benchmarks."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.grading import (
    BenchmarkResultSchema,
    ExecutiveSummaryResponse,
    PersonaSummaryResponse,
    RepositoryGradeReportResponse,
    TechnicalDebtSchema,
    TechnicalSummaryResponse,
)
from app.services.grading_service import GradingService, IQService
from app.tasks.repository_grading_tasks import repository_grading_task

router = APIRouter()


@router.post(
    "/{id}/grade",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger Repository Grade Analysis",
)
async def trigger_grade_analysis(id: uuid.UUID) -> dict[str, str]:
    """Trigger background CORTEX Grade Engine calculation."""
    repository_grading_task.delay(str(id))
    return {
        "message": "Repository Grade analysis triggered successfully",
        "repository_id": str(id),
    }


@router.get(
    "/{id}/grade",
    response_model=RepositoryGradeReportResponse,
    summary="Get Overall Repository Grade Report",
)
async def get_grade_report(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve CORTEX Repository Grade Report (A+ to F), 5-category breakdown, guardrail caps, and narrative summary."""
    return await GradingService.get_grade_report(db, id)


@router.get(
    "/{id}/persona-summary",
    response_model=PersonaSummaryResponse,
    summary="Get Persona-Based Summary",
)
async def get_persona_summary(
    id: uuid.UUID,
    persona: str = Query("general", description="Persona lens: executive, technical, recruiter, engineering_manager, general"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve summary report viewed through specific audience lens without altering underlying grades."""
    return await GradingService.get_persona_summary(db, id, persona=persona)


# Backward compatibility deprecated route /repositories/{id}/iq
@router.post(
    "/{id}/iq",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger Repository IQ Analysis (Deprecated - use /grade)",
    deprecated=True,
)
async def trigger_iq_analysis(id: uuid.UUID, response: Response) -> dict[str, str]:
    """Deprecated endpoint alias for /repositories/{id}/grade."""
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = f"</api/v1/repositories/{id}/grade>; rel=\"successor-version\""
    return await trigger_grade_analysis(id)


@router.get(
    "/{id}/iq",
    response_model=RepositoryGradeReportResponse,
    summary="Get Overall Repository IQ Report (Deprecated - use /grade)",
    deprecated=True,
)
async def get_iq_report(
    id: uuid.UUID,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Deprecated endpoint alias for /repositories/{id}/grade."""
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = f"</api/v1/repositories/{id}/grade>; rel=\"successor-version\""
    return await get_grade_report(id, db)


@router.get(
    "/{id}/executive-summary",
    response_model=ExecutiveSummaryResponse,
    summary="Get Executive Summary",
)
async def get_executive_summary(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve Executive Summary report."""
    return await GradingService.get_executive_summary(db, id)


@router.get(
    "/{id}/technical-summary",
    response_model=TechnicalSummaryResponse,
    summary="Get Technical Summary",
)
async def get_technical_summary(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve Technical Summary report."""
    return await GradingService.get_technical_summary(db, id)


@router.get(
    "/{id}/strengths",
    response_model=list[str],
    summary="Get Repository Strengths",
)
async def get_strengths(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve identified top repository strengths."""
    return await GradingService.get_strengths(db, id)


@router.get(
    "/{id}/weaknesses",
    response_model=list[str],
    summary="Get Repository Weaknesses",
)
async def get_weaknesses(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve identified top repository weaknesses."""
    return await GradingService.get_weaknesses(db, id)


@router.get(
    "/{id}/technical-debt",
    response_model=TechnicalDebtSchema,
    summary="Get Technical Debt Estimation",
)
async def get_technical_debt(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve technical debt estimation hours, days, breakdown, and finding items."""
    return await GradingService.get_technical_debt(db, id)


@router.get(
    "/{id}/benchmark",
    response_model=BenchmarkResultSchema,
    summary="Get Industry Benchmark Percentiles",
)
async def get_benchmark_percentiles(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retrieve benchmark percentile comparisons against industry standards."""
    return await GradingService.get_benchmark_percentiles(db, id)
