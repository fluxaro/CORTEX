"""Repository management API endpoints."""

import uuid
from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryListResponse,
    RepositoryResponse,
)
from app.services.repository_service import RepositoryService

router = APIRouter()


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new repository",
    description="Validate GitHub repository URL, retrieve metadata, store in database, and queue cloning pipeline.",
)
async def create_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
) -> RepositoryResponse:
    """Ingest a public GitHub repository."""
    repo = await RepositoryService.create_repository(db=db, url=payload.url)
    return RepositoryResponse.model_validate(repo)


@router.get(
    "",
    response_model=RepositoryListResponse,
    status_code=status.HTTP_200_OK,
    summary="List repositories",
    description="Retrieve paginated list of repositories with optional filtering and sorting.",
)
async def list_repositories(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Items per page"),
    status: str | None = Query(
        default=None, description="Filter by status (PENDING, CLONING, READY, FAILED)"
    ),
    owner: str | None = Query(default=None, description="Filter by repository owner"),
    language: str | None = Query(
        default=None, description="Filter by primary language"
    ),
    sort_by: Literal["created_at", "stars", "updated_at"] = Query(
        default="created_at", description="Field to sort by"
    ),
    order: Literal["asc", "desc"] = Query(default="desc", description="Sort order"),
    db: AsyncSession = Depends(get_db),
) -> RepositoryListResponse:
    """List ingested repositories."""
    data = await RepositoryService.list_repositories(
        db=db,
        page=page,
        page_size=page_size,
        status=status,
        owner=owner,
        language=language,
        sort_by=sort_by,
        order=order,
    )
    return RepositoryListResponse(
        items=[RepositoryResponse.model_validate(item) for item in data["items"]],
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        total_pages=data["total_pages"],
    )


@router.get(
    "/{id}",
    response_model=RepositoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get repository details",
    description="Retrieve repository details and file system index by UUID.",
)
async def get_repository(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> RepositoryResponse:
    """Get single repository by ID."""
    repo = await RepositoryService.get_repository_by_id(db=db, repository_id=id)
    return RepositoryResponse.model_validate(repo)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete repository",
    description="Delete repository record and its local cloned files.",
)
async def delete_repository(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete repository by ID."""
    await RepositoryService.delete_repository_by_id(db=db, repository_id=id)
