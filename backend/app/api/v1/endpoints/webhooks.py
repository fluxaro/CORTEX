"""Webhooks REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import WebhookCreateRequest, WebhookResponse
from app.services.git_platform_service import GitPlatformService

router = APIRouter()


@router.post("/{provider}", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(provider: str, payload: dict[str, Any]) -> Any:
    """Receive incoming webhook payload from GitHub, GitLab, or Bitbucket."""
    return {
        "status": "ACCEPTED",
        "provider": provider,
        "event": payload.get("event", "push"),
    }


@router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
async def register_webhook(
    req: WebhookCreateRequest, db: AsyncSession = Depends(get_db)
) -> Any:
    """Register a new repository webhook."""
    service = GitPlatformService(db)
    return await service.register_webhook(req)
