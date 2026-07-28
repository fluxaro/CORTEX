"""Audit Logs REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.enterprise import AuditLogResponse
from app.services.audit_log_service import AuditLogService

router = APIRouter()


@router.get("", response_model=list[AuditLogResponse])
async def list_audit_logs(
    workspace_id: str | None = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List immutable security audit log trail."""
    service = AuditLogService(db)
    return await service.list_audit_logs(workspace_id, limit)
