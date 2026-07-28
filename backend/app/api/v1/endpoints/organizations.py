"""Organizations REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import OrganizationCreateRequest, OrganizationResponse
from app.services.workspace_service import WorkspaceService

router = APIRouter()


@router.post(
    "", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED
)
async def create_organization(
    req: OrganizationCreateRequest,
    user_id: str = "mock-user-id",
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new enterprise organization."""
    service = WorkspaceService(db)
    org = await service.create_organization(user_id, req)
    return org
