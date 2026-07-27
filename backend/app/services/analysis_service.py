"""Static analysis service layer."""

import math
import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.custom_exceptions import RepositoryNotFoundError
from app.models.analysis import (
    AnalysisRun,
    AnalysisRunStatus,
    ClassMetrics,
    CodeSmell,
    FileMetrics,
    FunctionMetrics,
    RepositoryMetrics,
)
from app.models.repository import Repository
from app.tasks.analysis_tasks import static_analysis_task


class AnalysisService:
    """Service handling static analysis operations and metrics querying."""

    @staticmethod
    async def trigger_analysis(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> AnalysisRun:
        """Trigger a new static analysis run for a repository."""
        result = await db.execute(
            select(Repository).where(Repository.id == repository_id)
        )
        repo = result.scalar_one_or_none()
        if not repo:
            raise RepositoryNotFoundError(identifier=str(repository_id))

        analysis_run = AnalysisRun(
            repository_id=repository_id,
            status=AnalysisRunStatus.PENDING.value,
        )
        db.add(analysis_run)
        await db.commit()

        try:
            static_analysis_task.delay(str(analysis_run.id))
        except Exception:
            pass

        fetched = await db.execute(
            select(AnalysisRun)
            .options(selectinload(AnalysisRun.repository_metrics))
            .where(AnalysisRun.id == analysis_run.id)
        )
        return fetched.scalar_one()

    @staticmethod
    async def get_latest_analysis_run(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> AnalysisRun:
        """Get the latest analysis run for a repository."""
        result = await db.execute(
            select(AnalysisRun)
            .options(selectinload(AnalysisRun.repository_metrics))
            .where(AnalysisRun.repository_id == repository_id)
            .order_by(AnalysisRun.created_at.desc())
            .limit(1)
        )
        run = result.scalar_one_or_none()
        if not run:
            raise RepositoryNotFoundError(
                identifier=f"Analysis for repository {repository_id}"
            )
        return run

    @staticmethod
    async def get_repository_metrics(
        db: AsyncSession,
        repository_id: uuid.UUID,
        analysis_run_id: uuid.UUID | None = None,
    ) -> RepositoryMetrics:
        """Get repository metrics for a specific or latest analysis run."""
        query = select(RepositoryMetrics).where(
            RepositoryMetrics.repository_id == repository_id
        )
        if analysis_run_id:
            query = query.where(RepositoryMetrics.analysis_run_id == analysis_run_id)
        else:
            query = query.order_by(RepositoryMetrics.created_at.desc()).limit(1)

        result = await db.execute(query)
        metrics = result.scalar_one_or_none()
        if not metrics:
            raise RepositoryNotFoundError(
                identifier=f"Metrics for repository {repository_id}"
            )
        return metrics

    @staticmethod
    async def list_file_metrics(
        db: AsyncSession,
        repository_id: uuid.UUID,
        analysis_run_id: uuid.UUID | None = None,
        page: int = 1,
        page_size: int = 10,
        language: str | None = None,
        sort_by: str = "loc",
        order: str = "desc",
    ) -> dict[str, Any]:
        """List paginated file metrics for an analysis run."""
        if not analysis_run_id:
            latest_run = await AnalysisService.get_latest_analysis_run(
                db, repository_id
            )
            analysis_run_id = latest_run.id

        query = select(FileMetrics).where(
            FileMetrics.analysis_run_id == analysis_run_id
        )

        if language:
            query = query.where(func.lower(FileMetrics.language) == language.lower())

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        sort_col = getattr(FileMetrics, sort_by, FileMetrics.loc)
        query = query.order_by(
            sort_col.asc() if order.lower() == "asc" else sort_col.desc()
        )

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)
        items = list(result.scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_function_metrics(
        db: AsyncSession,
        repository_id: uuid.UUID,
        analysis_run_id: uuid.UUID | None = None,
        page: int = 1,
        page_size: int = 10,
        name: str | None = None,
        sort_by: str = "complexity",
        order: str = "desc",
    ) -> dict[str, Any]:
        """List paginated function metrics for an analysis run."""
        if not analysis_run_id:
            latest_run = await AnalysisService.get_latest_analysis_run(
                db, repository_id
            )
            analysis_run_id = latest_run.id

        query = select(FunctionMetrics).where(
            FunctionMetrics.analysis_run_id == analysis_run_id
        )

        if name:
            query = query.where(FunctionMetrics.name.ilike(f"%{name}%"))

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        sort_col = getattr(FunctionMetrics, sort_by, FunctionMetrics.complexity)
        query = query.order_by(
            sort_col.asc() if order.lower() == "asc" else sort_col.desc()
        )

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)
        items = list(result.scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_class_metrics(
        db: AsyncSession,
        repository_id: uuid.UUID,
        analysis_run_id: uuid.UUID | None = None,
        page: int = 1,
        page_size: int = 10,
        name: str | None = None,
        sort_by: str = "methods_count",
        order: str = "desc",
    ) -> dict[str, Any]:
        """List paginated class metrics for an analysis run."""
        if not analysis_run_id:
            latest_run = await AnalysisService.get_latest_analysis_run(
                db, repository_id
            )
            analysis_run_id = latest_run.id

        query = select(ClassMetrics).where(
            ClassMetrics.analysis_run_id == analysis_run_id
        )

        if name:
            query = query.where(ClassMetrics.name.ilike(f"%{name}%"))

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        sort_col = getattr(ClassMetrics, sort_by, ClassMetrics.methods_count)
        query = query.order_by(
            sort_col.asc() if order.lower() == "asc" else sort_col.desc()
        )

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)
        items = list(result.scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_code_smells(
        db: AsyncSession,
        repository_id: uuid.UUID,
        analysis_run_id: uuid.UUID | None = None,
        page: int = 1,
        page_size: int = 10,
        smell_type: str | None = None,
        severity: str | None = None,
    ) -> dict[str, Any]:
        """List paginated code smells for an analysis run."""
        if not analysis_run_id:
            latest_run = await AnalysisService.get_latest_analysis_run(
                db, repository_id
            )
            analysis_run_id = latest_run.id

        query = select(CodeSmell).where(CodeSmell.analysis_run_id == analysis_run_id)

        if smell_type:
            query = query.where(func.lower(CodeSmell.smell_type) == smell_type.lower())
        if severity:
            query = query.where(func.lower(CodeSmell.severity) == severity.lower())

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)
        items = list(result.scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }
