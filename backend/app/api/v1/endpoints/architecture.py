"""Architecture Intelligence API endpoints."""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.architecture import (
    ArchitectureAnalysisResponse,
    ArchitectureLayerResponse,
    DependencyGraphResponse,
    DetectedPatternListResponse,
    FrameworkDetectionResponse,
    TechnologyStackResponse,
)
from app.services.architecture_service import ArchitectureService

router = APIRouter()


@router.post(
    "/{id}/architecture",
    response_model=ArchitectureAnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger architecture analysis",
    description="Trigger Architecture Intelligence analysis for a repository.",
)
async def trigger_architecture_analysis(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ArchitectureAnalysisResponse:
    """Trigger architecture analysis."""
    arch = await ArchitectureService.trigger_architecture_analysis(
        db=db, repository_id=id
    )
    return ArchitectureAnalysisResponse.model_validate(arch)


@router.get(
    "/{id}/architecture",
    response_model=ArchitectureAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get latest architecture intelligence report",
    description="Retrieve status, architecture style, and raw architectural score components.",
)
async def get_latest_architecture(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ArchitectureAnalysisResponse:
    """Get latest architecture analysis."""
    arch = await ArchitectureService.get_latest_architecture(db=db, repository_id=id)
    return ArchitectureAnalysisResponse.model_validate(arch)


@router.get(
    "/{id}/patterns",
    response_model=DetectedPatternListResponse,
    status_code=status.HTTP_200_OK,
    summary="List detected design patterns",
    description="Retrieve paginated list of design patterns identified in codebase with confidence scores.",
)
async def list_patterns(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    category: str | None = Query(default=None),
    name: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> DetectedPatternListResponse:
    """List design patterns."""
    data = await ArchitectureService.list_patterns(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        category=category,
        name=name,
    )
    return DetectedPatternListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/layers",
    response_model=list[ArchitectureLayerResponse],
    status_code=status.HTTP_200_OK,
    summary="List architectural layers",
    description="Retrieve identified architectural layers and mapped files.",
)
async def list_layers(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[ArchitectureLayerResponse]:
    """List architectural layers."""
    layers = await ArchitectureService.list_layers(db=db, repository_id=id)
    return [ArchitectureLayerResponse.model_validate(layer) for layer in layers]


@router.get(
    "/{id}/dependency-graph",
    response_model=DependencyGraphResponse,
    status_code=status.HTTP_200_OK,
    summary="Get module dependency graph",
    description="Retrieve module dependency graph containing nodes and directed edges.",
)
async def get_dependency_graph(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> DependencyGraphResponse:
    """Get module dependency graph."""
    graph = await ArchitectureService.get_dependency_graph(db=db, repository_id=id)
    return DependencyGraphResponse.model_validate(graph)


@router.get(
    "/{id}/frameworks",
    response_model=list[FrameworkDetectionResponse],
    status_code=status.HTTP_200_OK,
    summary="List detected frameworks",
    description="Retrieve detected web/backend frameworks and framework convention validation findings.",
)
async def list_frameworks(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[FrameworkDetectionResponse]:
    """List frameworks."""
    frameworks = await ArchitectureService.list_frameworks(db=db, repository_id=id)
    return [FrameworkDetectionResponse.model_validate(f) for f in frameworks]


@router.get(
    "/{id}/technologies",
    response_model=TechnologyStackResponse,
    status_code=status.HTTP_200_OK,
    summary="Get extracted technology stack",
    description="Retrieve structured technology stack metadata.",
)
async def get_technology_stack(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> TechnologyStackResponse:
    """Get technology stack."""
    tech = await ArchitectureService.get_technology_stack(db=db, repository_id=id)
    return TechnologyStackResponse.model_validate(tech)
