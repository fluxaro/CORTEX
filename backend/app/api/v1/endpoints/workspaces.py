"""Workspaces REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import (
    InvitationCreateRequest,
    InvitationResponse,
    MembershipResponse,
    WorkspaceCreateRequest,
    WorkspaceResponse,
)
from app.services.workspace_service import WorkspaceService

router = APIRouter()


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    req: WorkspaceCreateRequest,
    user_id: str = "mock-user-id",
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new workspace."""
    service = WorkspaceService(db)
    ws = await service.create_workspace(user_id, req)
    return ws


@router.get("", response_model=list[WorkspaceResponse])
async def list_workspaces(
    user_id: str = "mock-user-id", db: AsyncSession = Depends(get_db)
) -> Any:
    """List workspaces for current user."""
    service = WorkspaceService(db)
    return await service.get_user_workspaces(user_id)


@router.get("/{id}/members", response_model=list[MembershipResponse])
async def list_members(id: str, db: AsyncSession = Depends(get_db)) -> Any:
    """List members of a workspace."""
    service = WorkspaceService(db)
    return await service.get_workspace_members(id)


@router.post(
    "/{id}/invitations",
    response_model=InvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def invite_member(
    id: str,
    req: InvitationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Invite member to workspace."""
    req.workspace_id = id
    service = WorkspaceService(db)
    return await service.invite_member(req)
