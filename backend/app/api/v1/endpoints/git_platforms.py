"""Git Platforms REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import GitRepoImportRequest
from app.schemas.repository import RepositoryResponse
from app.services.git_platform_service import GitPlatformService

router = APIRouter()


@router.post(
    "/{provider}/import",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def import_repo(
    provider: str,
    req: GitRepoImportRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Import repository from GitHub, GitLab, or Bitbucket."""
    req.provider = provider
    service = GitPlatformService(db)
    repo, _ = await service.import_repository(req)
    return repo
