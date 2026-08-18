"""Celery task for CORTEX Repository Grade Reports & AI Intelligence execution."""

import asyncio
import logging
import uuid

from sqlalchemy import select

from app.analyzers.grading.engine import RepositoryGradingEngine
from app.database.session import AsyncSessionLocal
from app.models.analysis import AnalysisRun, RepositoryMetrics
from app.models.architecture import ArchitectureAnalysis
from app.models.grading import (
    BenchmarkResult,
    EngineeringInsight,
    ExecutiveSummary,
    ImprovementRecommendation,
    RepositoryGradeReport,
    RepositorySummary,
    TechnicalDebt,
    TechnicalSummary,
)
from app.models.maintainability import (
    CiAnalysis,
    DocumentationAnalysis,
    GitHistoryAnalysis,
    MaintainabilityMetrics,
    TestingAnalysis,
)
from app.models.repository import Repository
from app.models.security import SecurityAnalysis
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _async_run_repository_grading(
    repository_id: str, run_id: str | None = None
) -> None:  # noqa: C901
    """Execute CORTEX Repository Grading pipeline."""
    repo_uuid = uuid.UUID(repository_id)
    async with AsyncSessionLocal() as session:
        # Load Repository
        r_stmt = select(Repository).where(Repository.id == repo_uuid)
        r_res = await session.execute(r_stmt)
        repo = r_res.scalar_one_or_none()
        if not repo:
            logger.error(
                f"Repository {repository_id} not found for Repository Grade analysis."
            )
            return

        logger.info(
            f"Repository Grade calculation started for repository {repo.full_name}"
        )

        # Find or create AnalysisRun
        if run_id:
            run_uuid = uuid.UUID(run_id)
        else:
            run_stmt = (
                select(AnalysisRun)
                .where(AnalysisRun.repository_id == repo_uuid)
                .order_by(AnalysisRun.created_at.desc())
                .limit(1)
            )
            run_res = await session.execute(run_stmt)
            latest_run = run_res.scalar_one_or_none()
            if latest_run:
                run_uuid = latest_run.id
            else:
                new_run = AnalysisRun(repository_id=repo_uuid, status="COMPLETED")
                session.add(new_run)
                await session.commit()
                run_uuid = new_run.id

        # Load subsystem metrics
        static_metrics = (
            await session.execute(
                select(RepositoryMetrics).where(
                    RepositoryMetrics.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        arch_analysis = (
            await session.execute(
                select(ArchitectureAnalysis).where(
                    ArchitectureAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        sec_analysis = (
            await session.execute(
                select(SecurityAnalysis).where(
                    SecurityAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        maint_metrics = (
            await session.execute(
                select(MaintainabilityMetrics).where(
                    MaintainabilityMetrics.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        doc_analysis = (
            await session.execute(
                select(DocumentationAnalysis).where(
                    DocumentationAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        test_analysis = (
            await session.execute(
                select(TestingAnalysis).where(
                    TestingAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        ci_analysis = (
            await session.execute(
                select(CiAnalysis).where(
                    CiAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        git_history = (
            await session.execute(
                select(GitHistoryAnalysis).where(
                    GitHistoryAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        # Run Grading Engine
        report = RepositoryGradingEngine.run(
            repo_name=repo.name,
            static_metrics=static_metrics,
            arch_analysis=arch_analysis,
            sec_analysis=sec_analysis,
            maint_metrics=maint_metrics,
            doc_analysis=doc_analysis,
            test_analysis=test_analysis,
            ci_analysis=ci_analysis,
            git_history=git_history,
            provider_type="mock",
        )

        # Cleanup existing grade report
        old_stmt = select(RepositoryGradeReport).where(
            RepositoryGradeReport.analysis_run_id == run_uuid
        )
        old_res = await session.execute(old_stmt)
        old_rec = old_res.scalar_one_or_none()
        if old_rec:
            await session.delete(old_rec)
            await session.flush()

        cat_dict = {
            "security": report.category_scores.security_score,
            "architecture": report.category_scores.architecture_score,
            "code_quality": report.category_scores.code_quality_score,
            "maintainability": report.category_scores.maintainability_score,
            "community_velocity": report.category_scores.community_velocity_score,
        }

        grade_rec = RepositoryGradeReport(
            repository_id=repo_uuid,
            analysis_run_id=run_uuid,
            overall_score=report.overall_score,
            overall_grade=report.overall_grade,
            capped=report.capped,
            cap_reason=report.cap_reason,
            maturity_level=report.maturity.level,
            category_scores=cat_dict,
            subsystem_scores=cat_dict,
        )
        session.add(grade_rec)
        await session.flush()

        session.add(
            RepositorySummary(
                repository_iq_id=grade_rec.id,
                executive_summary=report.executive_summary,
                technical_summary=report.technical_summary,
                architecture_summary=report.architecture_summary,
                security_summary=report.security_summary,
                maintainability_summary=report.maintainability_summary,
                recruiter_summary=report.recruiter_summary,
                engineering_manager_summary=report.engineering_manager_summary,
            )
        )

        session.add(
            EngineeringInsight(
                repository_iq_id=grade_rec.id,
                strengths=report.insights.strengths,
                weaknesses=report.insights.weaknesses,
            )
        )

        session.add(
            TechnicalDebt(
                repository_iq_id=grade_rec.id,
                total_hours=report.debt.total_hours,
                total_days=report.debt.total_days,
                category_breakdown=report.debt.category_breakdown,
            )
        )

        for rec in report.insights.recommendations:
            session.add(
                ImprovementRecommendation(
                    repository_iq_id=grade_rec.id,
                    category=rec.category,
                    title=rec.title,
                    description=rec.description,
                    timeframe=rec.timeframe,
                    priority=rec.priority,
                    difficulty=rec.difficulty,
                    estimated_hours=rec.estimated_hours,
                )
            )

        session.add(
            BenchmarkResult(
                repository_iq_id=grade_rec.id,
                overall_percentile=report.benchmark.overall_percentile,
                quality_percentile=report.benchmark.quality_percentile,
                security_percentile=report.benchmark.security_percentile,
                architecture_percentile=report.benchmark.architecture_percentile,
                maintainability_percentile=report.benchmark.maintainability_percentile,
            )
        )

        session.add(
            ExecutiveSummary(
                repository_iq_id=grade_rec.id,
                summary_text=report.executive_summary,
                report_json={
                    "overall_score": report.overall_score,
                    "overall_grade": report.overall_grade,
                    "maturity": report.maturity.level,
                },
            )
        )

        session.add(
            TechnicalSummary(
                repository_iq_id=grade_rec.id,
                summary_text=report.technical_summary,
                report_json={
                    "debt_hours": report.debt.total_hours,
                    "debt_days": report.debt.total_days,
                },
            )
        )

        await session.commit()
        logger.info(
            f"Repository Grade analysis finished for {repo.full_name}. Grade: {report.overall_grade} ({report.overall_score}/100)"
        )


@celery_app.task(
    name="tasks.repository_grading_tasks.compute_grade_report",
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)
def repository_grading_task(
    self: celery_app.Task, repository_id: str, run_id: str | None = None
) -> None:
    """Celery task computing CORTEX Grade Report."""
    try:
        asyncio.run(_async_run_repository_grading(repository_id, run_id))
    except Exception as exc:
        logger.error(
            f"Error computing Repository Grade report for {repository_id}: {exc}",
            exc_info=True,
        )
        raise self.retry(exc=exc)


# Backward compatibility task alias
repository_iq_task = repository_grading_task
