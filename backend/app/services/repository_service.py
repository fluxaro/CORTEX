"""Repository management service layer."""

import math
import os
import shutil
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.custom_exceptions import (
    RepositoryAlreadyExistsError,
    RepositoryNotFoundError,
)
from app.models.repository import Repository
from app.services.github_client import GitHubClient
from app.tasks.repository_tasks import clone_repository_task


def _ensure_datetime(val: Any) -> datetime | None:
    """Ensure value is a timezone-aware datetime instance."""
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, str):
        cleaned = val.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned)
    return None


class RepositoryService:
    """Service handling repository creation, retrieval, listing, and deletion."""

    @staticmethod
    async def create_repository(
        db: AsyncSession,
        url: str,
        github_client: GitHubClient | None = None,
    ) -> Repository:
        """Validate, fetch metadata, store in DB, and trigger cloning pipeline."""
        if github_client is None:
            github_client = GitHubClient()

        owner, repo_name = github_client.parse_github_url(url)
        full_name = f"{owner}/{repo_name}"

        # Duplicate detection check
        existing_result = await db.execute(
            select(Repository).where(
                func.lower(Repository.full_name) == full_name.lower()
            )
        )
        if existing_result.scalar_one_or_none():
            raise RepositoryAlreadyExistsError(full_name=full_name)

        # Fetch metadata from GitHub API
        metadata = await github_client.get_repository_metadata(owner, repo_name)

        now = datetime.now(UTC)
        created_at = _ensure_datetime(metadata.get("created_at")) or now
        updated_at = _ensure_datetime(metadata.get("updated_at")) or now
        last_pushed_at = _ensure_datetime(metadata.get("last_pushed_at"))

        # Create DB record
        repo = Repository(
            name=metadata["name"],
            owner=metadata["owner"],
            full_name=metadata["full_name"],
            description=metadata.get("description"),
            default_branch=metadata.get("default_branch", "main"),
            stars=metadata.get("stars", 0),
            forks=metadata.get("forks", 0),
            language=metadata.get("language"),
            license=metadata.get("license"),
            clone_url=metadata["clone_url"],
            html_url=metadata["html_url"],
            visibility=metadata.get("visibility", "public"),
            size=metadata.get("size", 0),
            created_at=created_at,
            updated_at=updated_at,
            last_pushed_at=last_pushed_at,
        )

        db.add(repo)
        await db.commit()

        # Dispatch background clone task
        try:
            clone_repository_task.delay(str(repo.id))
        except Exception:
            # Fallback if Celery broker is not running in sync mode / dev
            pass

        # Re-fetch with loaded relationship
        fetched_result = await db.execute(
            select(Repository)
            .options(selectinload(Repository.file_index))
            .where(Repository.id == repo.id)
        )
        return fetched_result.scalar_one()

    @staticmethod
    async def get_repository_by_id(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> Repository:
        """Retrieve a repository by UUID including its file index."""
        result = await db.execute(
            select(Repository)
            .options(selectinload(Repository.file_index))
            .where(Repository.id == repository_id)
        )
        repo = result.scalar_one_or_none()
        if not repo:
            raise RepositoryNotFoundError(identifier=str(repository_id))
        return repo

    @staticmethod
    async def list_repositories(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        status: str | None = None,
        owner: str | None = None,
        language: str | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> dict[str, Any]:
        """List repositories with filtering, pagination, and sorting."""
        query = select(Repository).options(selectinload(Repository.file_index))

        # Filtering
        if status:
            query = query.where(Repository.status == status.upper())
        if owner:
            query = query.where(func.lower(Repository.owner) == owner.lower())
        if language:
            query = query.where(func.lower(Repository.language) == language.lower())

        # Count total items matching filters
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        # Sorting
        sort_column: Any = getattr(Repository, sort_by, Repository.created_at)
        if order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)
        items = list(result.scalars().all())

        total_pages = math.ceil(total / page_size) if page_size > 0 else 1

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(total_pages, 1),
        }

    @staticmethod
    async def delete_repository_by_id(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> None:
        """Delete a repository from DB and remove its local clone storage."""
        result = await db.execute(
            select(Repository).where(Repository.id == repository_id)
        )
        repo = result.scalar_one_or_none()
        if not repo:
            raise RepositoryNotFoundError(identifier=str(repository_id))

        # Delete local clone directory if present
        if repo.local_path and os.path.exists(repo.local_path):
            shutil.rmtree(repo.local_path, ignore_errors=True)

        await db.delete(repo)
        await db.commit()
