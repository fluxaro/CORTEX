"""Notifications REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    user_id: str = "mock-user-id",
    unread_only: bool = False,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List in-app notifications for user."""
    service = NotificationService(db)
    return await service.get_user_notifications(user_id, unread_only)


@router.put("/{id}/read", response_model=NotificationResponse)
async def mark_read(id: str, db: AsyncSession = Depends(get_db)) -> Any:
    """Mark a notification as read."""
    service = NotificationService(db)
    notif = await service.mark_as_read(id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return notif
