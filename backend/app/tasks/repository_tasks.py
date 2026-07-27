"""Celery background tasks for repository acquisition and analysis preparation."""

import asyncio
import logging
import os
import uuid

from sqlalchemy import select

from app.core.config.settings import settings
from app.database.session import AsyncSessionLocal
from app.models.repository import (
    AnalysisStatus,
    Repository,
    RepositoryFileIndex,
    RepositoryStatus,
)
from app.services.git_service import GitService
from app.services.indexer_service import FileIndexerService
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _async_clone_repository(repository_id_str: str) -> None:
    """Async implementation of clone_repository_task."""
    repo_uuid = uuid.UUID(repository_id_str)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Repository).where(Repository.id == repo_uuid)
        )
        repo = result.scalar_one_or_none()
        if not repo:
            logger.error(
                f"Task error: Repository {repository_id_str} not found in database."
            )
            return

        repo.status = RepositoryStatus.CLONING.value
        await session.commit()

        target_dir = os.path.join(settings.STORAGE_DIR, str(repo.id))

        try:
            # Step 1: Clone repository
            cloned_path = GitService.clone_repository(
                clone_url=repo.clone_url,
                target_path=target_dir,
                branch=repo.default_branch,
            )

            # Step 2: Generate file system index
            index_data = FileIndexerService.index_directory(cloned_path)

            # Step 3: Upsert File Index in DB
            idx_result = await session.execute(
                select(RepositoryFileIndex).where(
                    RepositoryFileIndex.repository_id == repo_uuid
                )
            )
            file_index = idx_result.scalar_one_or_none()

            if not file_index:
                file_index = RepositoryFileIndex(
                    repository_id=repo_uuid,
                    folder_count=index_data["folder_count"],
                    file_count=index_data["file_count"],
                    max_depth=index_data["max_depth"],
                    total_size_bytes=index_data["total_size_bytes"],
                    largest_files=index_data["largest_files"],
                    file_extensions=index_data["file_extensions"],
                    language_distribution=index_data["language_distribution"],
                )
                session.add(file_index)
            else:
                file_index.folder_count = index_data["folder_count"]
                file_index.file_count = index_data["file_count"]
                file_index.max_depth = index_data["max_depth"]
                file_index.total_size_bytes = index_data["total_size_bytes"]
                file_index.largest_files = index_data["largest_files"]
                file_index.file_extensions = index_data["file_extensions"]
                file_index.language_distribution = index_data["language_distribution"]

            # Step 4: Update Repository status to READY
            repo.status = RepositoryStatus.READY.value
            repo.local_path = cloned_path
            await session.commit()

            logger.info(f"Repository {repo.full_name} successfully cloned and indexed.")

            # Step 5: Queue preparation job
            prepare_analysis_task.delay(repository_id_str)

        except Exception as exc:
            logger.exception(f"Failed to clone repository {repository_id_str}: {exc}")
            repo.status = RepositoryStatus.FAILED.value
            await session.commit()


async def _async_prepare_analysis(repository_id_str: str) -> None:
    """Async implementation of prepare_analysis_task."""
    repo_uuid = uuid.UUID(repository_id_str)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Repository).where(Repository.id == repo_uuid)
        )
        repo = result.scalar_one_or_none()
        if not repo:
            logger.error(
                f"Task error: Repository {repository_id_str} not found in database."
            )
            return

        from app.models.analysis import AnalysisRun, AnalysisRunStatus
        from app.tasks.analysis_tasks import static_analysis_task

        repo.analysis_status = AnalysisStatus.QUEUED.value

        analysis_run = AnalysisRun(
            repository_id=repo.id,
            status=AnalysisRunStatus.PENDING.value,
        )
        session.add(analysis_run)
        await session.commit()
        await session.refresh(analysis_run)

        logger.info(
            f"Repository {repo.full_name} analysis status set to QUEUED (Run ID: {analysis_run.id})."
        )
        try:
            static_analysis_task.delay(str(analysis_run.id))
        except Exception:
            pass


@celery_app.task(name="app.tasks.repository_tasks.clone_repository_task")
def clone_repository_task(repository_id: str) -> None:
    """Celery task to clone repository and index file system."""
    asyncio.run(_async_clone_repository(repository_id))


@celery_app.task(name="app.tasks.repository_tasks.prepare_analysis_task")
def prepare_analysis_task(repository_id: str) -> None:
    """Celery task placeholder to prepare repository for future analyzer phases."""
    asyncio.run(_async_prepare_analysis(repository_id))
