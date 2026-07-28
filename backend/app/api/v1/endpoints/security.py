"""Security Intelligence API endpoints."""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.security import (
    AuthenticationFindingListResponse,
    AuthorizationFindingListResponse,
    ConfigurationFindingListResponse,
    DependencyFindingListResponse,
    SecretFindingListResponse,
    SecurityAnalysisResponse,
    SecurityFindingListResponse,
)
from app.services.security_service import SecurityService

router = APIRouter()


@router.post(
    "/{id}/security",
    response_model=SecurityAnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger security analysis",
    description="Trigger Security Intelligence (SAST) analysis for a repository.",
)
async def trigger_security_analysis(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> SecurityAnalysisResponse:
    """Trigger security analysis."""
    sec = await SecurityService.trigger_security_analysis(db=db, repository_id=id)
    return SecurityAnalysisResponse.model_validate(sec)


@router.get(
    "/{id}/security",
    response_model=SecurityAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get latest security report & raw metrics",
    description="Retrieve overall security report, finding counts by severity, secrets count, and dependency vulnerabilities.",
)
async def get_latest_security(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> SecurityAnalysisResponse:
    """Get latest security report."""
    sec = await SecurityService.get_latest_security(db=db, repository_id=id)
    return SecurityAnalysisResponse.model_validate(sec)


@router.get(
    "/{id}/security/findings",
    response_model=SecurityFindingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List SAST security findings",
    description="Retrieve paginated SAST findings filterable by severity, language, and category.",
)
async def list_findings(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    severity: str | None = Query(default=None),
    language: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> SecurityFindingListResponse:
    """List SAST findings."""
    data = await SecurityService.list_findings(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        severity=severity,
        language=language,
        category=category,
    )
    return SecurityFindingListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/security/secrets",
    response_model=SecretFindingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List committed secrets",
    description="Retrieve paginated exposed secrets and API tokens with masked values and entropy scores.",
)
async def list_secrets(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    secret_type: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> SecretFindingListResponse:
    """List secret findings."""
    data = await SecurityService.list_secrets(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        secret_type=secret_type,
        severity=severity,
    )
    return SecretFindingListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/security/dependencies",
    response_model=DependencyFindingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List dependency vulnerabilities",
    description="Retrieve paginated vulnerable package dependencies and CVE information.",
)
async def list_dependencies(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    severity: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> DependencyFindingListResponse:
    """List dependency findings."""
    data = await SecurityService.list_dependencies(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        severity=severity,
    )
    return DependencyFindingListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/security/configuration",
    response_model=ConfigurationFindingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List configuration findings",
    description="Retrieve paginated infrastructure configuration findings.",
)
async def list_configurations(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    severity: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> ConfigurationFindingListResponse:
    """List configuration findings."""
    data = await SecurityService.list_configurations(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        severity=severity,
    )
    return ConfigurationFindingListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/security/authentication",
    response_model=AuthenticationFindingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List authentication findings",
    description="Retrieve paginated authentication weaknesses and password hashing findings.",
)
async def list_authentication(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    severity: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> AuthenticationFindingListResponse:
    """List authentication findings."""
    data = await SecurityService.list_authentication(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        severity=severity,
    )
    return AuthenticationFindingListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}/security/authorization",
    response_model=AuthorizationFindingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List authorization findings",
    description="Retrieve paginated authorization weaknesses and RBAC findings.",
)
async def list_authorization(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    severity: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> AuthorizationFindingListResponse:
    """List authorization findings."""
    data = await SecurityService.list_authorization(
        db=db,
        repository_id=id,
        page=page,
        page_size=page_size,
        severity=severity,
    )
    return AuthorizationFindingListResponse(
        items=data["items"],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )
