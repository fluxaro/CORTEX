"""Git platform (GitHub, GitLab, Bitbucket) integration service."""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import RepositorySync, Webhook
from app.models.repository import Repository
from app.schemas.enterprise import GitRepoImportRequest, WebhookCreateRequest


class GitPlatformService:
    """Service for managing remote repositories, sync status, and webhooks."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def import_repository(
        self, req: GitRepoImportRequest
    ) -> tuple[Repository, RepositorySync]:
        """Import remote repository from GitHub, GitLab, or Bitbucket."""
        # 1. Create Repository record
        repo = Repository(
            name=req.name,
            owner=req.repo_url.split("/")[-2] if "/" in req.repo_url else "owner",
            full_name=f"{req.name}",
            clone_url=req.repo_url,
            html_url=req.repo_url,
            default_branch=req.default_branch,
            status="PENDING",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(repo)
        await self.session.flush()

        # 2. Create Sync record
        sync = RepositorySync(
            repository_id=str(repo.id),
            provider=req.provider.upper(),
            external_repo_id=req.external_repo_id,
            default_branch=req.default_branch,
            sync_status="SYNCED",
        )
        self.session.add(sync)
        await self.session.commit()
        await self.session.refresh(repo)
        await self.session.refresh(sync)
        return repo, sync

    async def register_webhook(self, req: WebhookCreateRequest) -> Webhook:
        """Register webhook endpoint for a repository."""
        webhook = Webhook(
            repository_id=req.repository_id,
            provider=req.provider.upper(),
            url=req.url,
            secret=req.secret,
            event_types={"events": req.event_types},
            is_active=True,
        )
        self.session.add(webhook)

        # Update sync record
        stmt = select(RepositorySync).where(
            RepositorySync.repository_id == req.repository_id
        )
        res = await self.session.execute(stmt)
        sync = res.scalars().first()
        if sync:
            sync.webhook_active = True

        await self.session.commit()
        await self.session.refresh(webhook)
        return webhook

    async def list_webhooks(self, repository_id: str) -> list[Webhook]:
        """List active webhooks for a repository."""
        stmt = select(Webhook).where(Webhook.repository_id == repository_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
