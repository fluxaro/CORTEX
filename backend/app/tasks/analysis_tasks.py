"""Celery background task for running static code analysis."""

import asyncio
import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.analyzers.base.engine import StaticAnalysisEngine
from app.database.session import AsyncSessionLocal
from app.models.analysis import (
    AnalysisRun,
    AnalysisRunStatus,
    ClassMetrics,
    CodeSmell,
    DuplicateFile,
    DuplicateGroup,
    FileMetrics,
    FunctionMetrics,
    RepositoryMetrics,
)
from app.models.repository import AnalysisStatus, Repository
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _async_run_static_analysis(analysis_run_id_str: str) -> None:  # noqa: C901
    """Async execution of static code analysis."""
    run_uuid = uuid.UUID(analysis_run_id_str)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AnalysisRun)
            .options(selectinload(AnalysisRun.repository_metrics))
            .where(AnalysisRun.id == run_uuid)
        )
        analysis_run = result.scalar_one_or_none()

        if not analysis_run:
            logger.error(f"AnalysisRun {analysis_run_id_str} not found in database.")
            return

        repo_result = await session.execute(
            select(Repository).where(Repository.id == analysis_run.repository_id)
        )
        repo = repo_result.scalar_one_or_none()

        if not repo or not repo.local_path:
            analysis_run.status = AnalysisRunStatus.FAILED.value
            analysis_run.error_message = (
                "Repository local storage path not found or repository not cloned."
            )
            await session.commit()
            return

        # Mark as RUNNING
        analysis_run.status = AnalysisRunStatus.RUNNING.value
        analysis_run.started_at = datetime.now(UTC)
        repo.analysis_status = AnalysisStatus.IN_PROGRESS.value
        await session.commit()

        logger.info(
            f"Starting static analysis for repository {repo.full_name} (Run ID: {analysis_run_id_str})"
        )

        try:
            engine = StaticAnalysisEngine(target_path=repo.local_path)
            report = engine.run()

            # 1. Store Repository Metrics
            repo_metrics = RepositoryMetrics(
                analysis_run_id=run_uuid,
                repository_id=repo.id,
                total_files=report.total_files,
                source_files=report.source_files,
                test_files=report.test_files,
                blank_lines=report.blank_lines,
                comment_lines=report.comment_lines,
                code_lines=report.code_lines,
                total_loc=report.total_loc,
                comment_ratio=report.comment_ratio,
                avg_complexity=report.avg_complexity,
                max_complexity=report.max_complexity,
                complexity_rank=report.complexity_rank,
                maintainability_index=report.maintainability_index,
                duplicate_percentage=report.duplicate_percentage,
                file_extension_dist=report.file_extension_dist,
                language_dist=report.language_dist,
            )
            session.add(repo_metrics)

            # 2. Store File Metrics & Function/Class Metrics
            for file_res in report.file_results:
                f_metric = FileMetrics(
                    analysis_run_id=run_uuid,
                    repository_id=repo.id,
                    path=file_res.path,
                    language=file_res.language,
                    loc=file_res.loc,
                    comment_lines=file_res.comment_lines,
                    blank_lines=file_res.blank_lines,
                    code_lines=file_res.code_lines,
                    function_count=file_res.function_count,
                    class_count=file_res.class_count,
                    import_count=file_res.import_count,
                    file_size=file_res.file_size,
                    complexity=file_res.complexity,
                    maintainability_index=file_res.maintainability_index,
                )
                session.add(f_metric)
                await session.flush()  # assign ID to f_metric

                for func_res in file_res.functions:
                    fn_metric = FunctionMetrics(
                        analysis_run_id=run_uuid,
                        repository_id=repo.id,
                        file_metrics_id=f_metric.id,
                        name=func_res.name,
                        class_name=func_res.class_name,
                        parameters=func_res.parameters,
                        return_annotation=func_res.return_annotation,
                        decorators=func_res.decorators,
                        visibility=func_res.visibility,
                        method_type=func_res.method_type,
                        line_count=func_res.line_count,
                        complexity=func_res.complexity,
                        nesting_depth=func_res.nesting_depth,
                        maintainability=func_res.maintainability,
                    )
                    session.add(fn_metric)

                for cls_res in file_res.classes:
                    cls_metric = ClassMetrics(
                        analysis_run_id=run_uuid,
                        repository_id=repo.id,
                        file_metrics_id=f_metric.id,
                        name=cls_res.name,
                        base_classes=cls_res.base_classes,
                        methods_count=cls_res.methods_count,
                        fields_count=cls_res.fields_count,
                        property_count=cls_res.property_count,
                        public_methods=cls_res.public_methods,
                        private_methods=cls_res.private_methods,
                        static_methods=cls_res.static_methods,
                        abstract_methods=cls_res.abstract_methods,
                    )
                    session.add(cls_metric)

            # 3. Store Duplicate Groups
            for dup_group in report.duplicate_groups:
                group_record = DuplicateGroup(
                    analysis_run_id=run_uuid,
                    repository_id=repo.id,
                    duplicate_hash=dup_group.duplicate_hash,
                    line_count=dup_group.line_count,
                    instance_count=dup_group.instance_count,
                )
                session.add(group_record)
                await session.flush()

                for loc in dup_group.locations:
                    dup_file = DuplicateFile(
                        duplicate_group_id=group_record.id,
                        file_path=loc.file_path,
                        start_line=loc.start_line,
                        end_line=loc.end_line,
                    )
                    session.add(dup_file)

            # 4. Store Code Smells
            for smell_res in report.code_smells:
                smell_record = CodeSmell(
                    analysis_run_id=run_uuid,
                    repository_id=repo.id,
                    file_path=smell_res.file_path,
                    smell_type=smell_res.smell_type,
                    severity=smell_res.severity,
                    line_number=smell_res.line_number,
                    symbol_name=smell_res.symbol_name,
                    description=smell_res.description,
                )
                session.add(smell_record)

            # Mark Run Completed
            analysis_run.status = AnalysisRunStatus.COMPLETED.value
            analysis_run.completed_at = datetime.now(UTC)
            repo.analysis_status = AnalysisStatus.COMPLETED.value
            await session.commit()

            logger.info(
                f"Static analysis completed successfully for repository {repo.full_name}"
            )
            from app.tasks.architecture_tasks import architecture_analysis_task

            try:
                architecture_analysis_task.delay(str(repo.id), str(run_uuid))
            except Exception:
                pass

        except Exception as exc:
            logger.exception(
                f"Static analysis failed for repository {repo.full_name}: {exc}"
            )
            analysis_run.status = AnalysisRunStatus.FAILED.value
            analysis_run.error_message = str(exc)
            repo.analysis_status = AnalysisStatus.FAILED.value
            await session.commit()


@celery_app.task(name="app.tasks.analysis_tasks.static_analysis_task")
def static_analysis_task(analysis_run_id: str) -> None:
    """Celery background task for running static analysis pipeline."""
    asyncio.run(_async_run_static_analysis(analysis_run_id))
