"""Workspace & Organization service."""

import uuid
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import (
    Invitation,
    Membership,
    Organization,
    Workspace,
)
from app.schemas.enterprise import (
    InvitationCreateRequest,
    OrganizationCreateRequest,
    WorkspaceCreateRequest,
)


class WorkspaceService:
    """Service managing Workspaces, Organizations, Memberships, and Invitations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_organization(
        self, owner_id: str, req: OrganizationCreateRequest
    ) -> Organization:
        """Create new enterprise organization."""
        org = Organization(
            name=req.name,
            slug=req.slug,
            avatar_url=req.avatar_url,
            owner_id=owner_id,
        )
        self.session.add(org)
        await self.session.flush()

        # Add owner membership
        member = Membership(
            user_id=owner_id,
            organization_id=org.id,
            role="OWNER",
            status="ACTIVE",
        )
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(org)
        return org

    async def create_workspace(
        self, owner_id: str, req: WorkspaceCreateRequest
    ) -> Workspace:
        """Create personal or organization workspace."""
        ws = Workspace(
            name=req.name,
            slug=req.slug,
            type=req.type,
            organization_id=req.organization_id,
            owner_id=owner_id,
        )
        self.session.add(ws)
        await self.session.flush()

        member = Membership(
            user_id=owner_id,
            workspace_id=ws.id,
            organization_id=req.organization_id,
            role="OWNER",
            status="ACTIVE",
        )
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(ws)
        return ws

    async def get_user_workspaces(self, user_id: str) -> list[Workspace]:
        """List all workspaces accessible to user."""
        stmt = (
            select(Workspace)
            .join(Membership, Membership.workspace_id == Workspace.id)
            .where(Membership.user_id == user_id)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def invite_member(self, req: InvitationCreateRequest) -> Invitation:
        """Create invitation for workspace or organization."""
        invitation = Invitation(
            email=req.email,
            workspace_id=req.workspace_id,
            organization_id=req.organization_id,
            role=req.role,
            token=str(uuid.uuid4()),
            status="PENDING",
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
        self.session.add(invitation)
        await self.session.commit()
        await self.session.refresh(invitation)
        return invitation

    async def get_workspace_members(self, workspace_id: str) -> list[Membership]:
        """List active members of a workspace."""
        stmt = select(Membership).where(Membership.workspace_id == workspace_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
