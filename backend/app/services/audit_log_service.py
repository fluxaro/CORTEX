"""Immutable Audit Log Service."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import AuditLog


class AuditLogService:
    """Service writing and retrieving security audit events."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_event(
        self,
        action: str,
        entity_type: str,
        user_id: str | None = None,
        workspace_id: str | None = None,
        entity_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditLog:
        """Write immutable audit log record."""
        audit = AuditLog(
            action=action,
            entity_type=entity_type,
            user_id=user_id,
            workspace_id=workspace_id,
            entity_id=entity_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details_json=details,
        )
        self.session.add(audit)
        await self.session.commit()
        await self.session.refresh(audit)
        return audit

    async def list_audit_logs(
        self, workspace_id: str | None = None, limit: int = 100
    ) -> list[AuditLog]:
        """Fetch chronological audit trail."""
        stmt = select(AuditLog)
        if workspace_id:
            stmt = stmt.where(AuditLog.workspace_id == workspace_id)
        stmt = stmt.order_by(AuditLog.created_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
