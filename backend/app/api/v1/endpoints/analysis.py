"""Static analysis API endpoints."""

import uuid
from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.analysis import (
    AnalysisRunResponse,
    ClassMetricsListResponse,
    CodeSmellListResponse,
    FileMetricsListResponse,
    FunctionMetricsListResponse,
    RepositoryMetricsResponse,
)
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.post(
    "/{id}/analyze",
    response_model=AnalysisRunResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger repository static analysis",
    description="Trigger a new static code analysis run for a repository.",
)
async def trigger_analysis(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> AnalysisRunResponse:
    """Trigger static code analysis."""
    run = await AnalysisService.trigger_analysis(db=db, repository_id=id)
    return AnalysisRunResponse.model_validate(run)


@router.get(
    "/{id}/analysis",
    response_model=AnalysisRunResponse,
    status_code=status.HTTP_200_OK,
    summary="Get latest analysis run status",
    description="Retrieve status of the latest analysis run for a repository.",
)
async def get_latest_analysis(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> AnalysisRunResponse:
    """Get latest analysis run."""
    run = await AnalysisService.get_latest_analysis_run(db=db, repository_id=id)
    return AnalysisRunResponse.model_validate(run)


@router.get(
    "/{id}/metrics",
    response_model=RepositoryMetricsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get repository metrics",
    description="Retrieve aggregated engineering metrics for a repository.",
)
async def get_repository_metrics(
    id: uuid.UUID,
    analysis_run_id: uuid.UUID | None = Query(
        default=None, description="Optional analysis run ID"
    ),
    db: AsyncSession = Depends(get_db),
) -> RepositoryMetricsResponse:
    """Get repository level metrics."""
    metrics = await AnalysisService.get_repository_metrics(
        db=db, repository_id=id, analysis_run_id=analysis_run_id
    )
    return RepositoryMetricsResponse.model_validate(metrics)


@router.get(
    "/{id}/files",
    response_model=FileMetricsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List file level metrics",
    description="Retrieve paginated file-level metrics for a repository analysis run.",
)
async def list_file_metrics(
    id: uuid.UUID,
    analysis_run_id: uuid.UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    language: str | None = Query(default=None),
    sort_by: Literal["loc", "complexity", "maintainability_index", "file_size"] = Query(
        default="loc"
    ),
    order: Literal["asc", "desc"] = Query(default="desc"),
    db: AsyncSession = Depends(get_db),
) -> FileMetricsListResponse:
    """List file metrics."""
    data = await AnalysisService.list_file_metrics(
        db=db,
        repository_id=id,
        analysis_run_id=analysis_run_id,
        page=page,
        page_size=page_size,
        language=language,
        sort_by=sort_by,
        order=order,
    )
    return FileMetricsListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/functions",
    response_model=FunctionMetricsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List function level metrics",
    description="Retrieve paginated function-level metrics.",
)
async def list_function_metrics(
    id: uuid.UUID,
    analysis_run_id: uuid.UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    name: str | None = Query(default=None),
    sort_by: Literal[
        "complexity", "line_count", "nesting_depth", "maintainability"
    ] = Query(default="complexity"),
    order: Literal["asc", "desc"] = Query(default="desc"),
    db: AsyncSession = Depends(get_db),
) -> FunctionMetricsListResponse:
    """List function metrics."""
    data = await AnalysisService.list_function_metrics(
        db=db,
        repository_id=id,
        analysis_run_id=analysis_run_id,
        page=page,
        page_size=page_size,
        name=name,
        sort_by=sort_by,
        order=order,
    )
    return FunctionMetricsListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/classes",
    response_model=ClassMetricsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List class level metrics",
    description="Retrieve paginated class-level metrics.",
)
async def list_class_metrics(
    id: uuid.UUID,
    analysis_run_id: uuid.UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    name: str | None = Query(default=None),
    sort_by: Literal["methods_count", "fields_count", "public_methods"] = Query(
        default="methods_count"
    ),
    order: Literal["asc", "desc"] = Query(default="desc"),
    db: AsyncSession = Depends(get_db),
) -> ClassMetricsListResponse:
    """List class metrics."""
    data = await AnalysisService.list_class_metrics(
        db=db,
        repository_id=id,
        analysis_run_id=analysis_run_id,
        page=page,
        page_size=page_size,
        name=name,
        sort_by=sort_by,
        order=order,
    )
    return ClassMetricsListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/smells",
    response_model=CodeSmellListResponse,
    status_code=status.HTTP_200_OK,
    summary="List code smells",
    description="Retrieve paginated code smells identified for a repository.",
)
async def list_code_smells(
    id: uuid.UUID,
    analysis_run_id: uuid.UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    smell_type: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> CodeSmellListResponse:
    """List code smells."""
    data = await AnalysisService.list_code_smells(
        db=db,
        repository_id=id,
        analysis_run_id=analysis_run_id,
        page=page,
        page_size=page_size,
        smell_type=smell_type,
        severity=severity,
    )
    return CodeSmellListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )
