"""In-App Notification Service."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import Notification


class NotificationService:
    """Service managing user notifications."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = "INFO",
        metadata: dict[str, Any] | None = None,
    ) -> Notification:
        """Create in-app notification for a user."""
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            is_read=False,
            metadata_json=metadata,
        )
        self.session.add(notif)
        await self.session.commit()
        await self.session.refresh(notif)
        return notif

    async def get_user_notifications(
        self, user_id: str, unread_only: bool = False
    ) -> list[Notification]:
        """List notifications for a user."""
        stmt = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            stmt = stmt.where(Notification.is_read.is_(False))
        stmt = stmt.order_by(Notification.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def mark_as_read(self, notification_id: str) -> Notification | None:
        """Mark notification as read."""
        stmt = select(Notification).where(Notification.id == notification_id)
        res = await self.session.execute(stmt)
        notif = res.scalars().first()
        if notif:
            notif.is_read = True
            await self.session.commit()
            await self.session.refresh(notif)
        return notif
