"""Maintainability & Repository Intelligence API endpoints."""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.maintainability import (
    CiAnalysisResponse,
    CommitAnalysisResponse,
    CommunityAnalysisResponse,
    DocumentationAnalysisResponse,
    GitHistoryAnalysisResponse,
    MaintainabilityMetricsResponse,
    ReleaseAnalysisResponse,
    RepositoryHealthResponse,
    TestingAnalysisResponse,
)
from app.services.maintainability_service import MaintainabilityService

router = APIRouter()


@router.post(
    "/{id}/maintainability",
    response_model=MaintainabilityMetricsResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger maintainability analysis",
    description="Trigger Maintainability & Repository Intelligence analysis for a repository.",
)
async def trigger_maintainability_analysis(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> MaintainabilityMetricsResponse:
    """Trigger maintainability analysis."""
    m = await MaintainabilityService.trigger_maintainability_analysis(
        db=db, repository_id=id
    )
    return MaintainabilityMetricsResponse.model_validate(m)


@router.get(
    "/{id}/maintainability",
    response_model=MaintainabilityMetricsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get latest maintainability metrics",
    description="Retrieve raw subsystem scores for documentation, testing, CI, releases, health, and community.",
)
async def get_latest_maintainability(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> MaintainabilityMetricsResponse:
    """Get latest maintainability metrics."""
    m = await MaintainabilityService.get_latest_maintainability(db=db, repository_id=id)
    return MaintainabilityMetricsResponse.model_validate(m)


@router.get(
    "/{id}/documentation",
    response_model=DocumentationAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get documentation analysis",
    description="Retrieve documentation completeness, README section breakdown, and doc generators.",
)
async def get_documentation(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> DocumentationAnalysisResponse:
    """Get documentation report."""
    doc = await MaintainabilityService.get_documentation(db=db, repository_id=id)
    return DocumentationAnalysisResponse.model_validate(doc)


@router.get(
    "/{id}/testing",
    response_model=TestingAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get testing analysis",
    description="Retrieve test framework findings, file counts, and test maturity score.",
)
async def get_testing(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> TestingAnalysisResponse:
    """Get testing report."""
    t = await MaintainabilityService.get_testing(db=db, repository_id=id)
    return TestingAnalysisResponse.model_validate(t)


@router.get(
    "/{id}/git-history",
    response_model=GitHistoryAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Git history analytics",
    description="Retrieve commit frequency, contributors count, repo age, and development velocity.",
)
async def get_git_history(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> GitHistoryAnalysisResponse:
    """Get Git history report."""
    gh = await MaintainabilityService.get_git_history(db=db, repository_id=id)
    return GitHistoryAnalysisResponse.model_validate(gh)


@router.get(
    "/{id}/commits",
    response_model=CommitAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get commit quality analysis",
    description="Retrieve Conventional Commits percentage, generic commit percentage, and quality score.",
)
async def get_commits(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> CommitAnalysisResponse:
    """Get commit analysis report."""
    ca = await MaintainabilityService.get_commits(db=db, repository_id=id)
    return CommitAnalysisResponse.model_validate(ca)


@router.get(
    "/{id}/releases",
    response_model=ReleaseAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get release analysis",
    description="Retrieve tag counts, SemVer compliance, and release cadence.",
)
async def get_releases(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ReleaseAnalysisResponse:
    """Get release report."""
    rel = await MaintainabilityService.get_releases(db=db, repository_id=id)
    return ReleaseAnalysisResponse.model_validate(rel)


@router.get(
    "/{id}/ci",
    response_model=CiAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get CI/CD analysis",
    description="Retrieve detected CI automation providers and job breakdown.",
)
async def get_ci(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> CiAnalysisResponse:
    """Get CI/CD report."""
    ci = await MaintainabilityService.get_ci(db=db, repository_id=id)
    return CiAnalysisResponse.model_validate(ci)


@router.get(
    "/{id}/community",
    response_model=CommunityAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get community standards analysis",
    description="Retrieve open source governance files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY).",
)
async def get_community(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> CommunityAnalysisResponse:
    """Get community report."""
    comm = await MaintainabilityService.get_community(db=db, repository_id=id)
    return CommunityAnalysisResponse.model_validate(comm)


@router.get(
    "/{id}/repository-health",
    response_model=RepositoryHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Get repository health report",
    description="Retrieve raw repository health breakdown metrics.",
)
async def get_repository_health(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> RepositoryHealthResponse:
    """Get repository health report."""
    rh = await MaintainabilityService.get_repository_health(db=db, repository_id=id)
    return RepositoryHealthResponse.model_validate(rh)
