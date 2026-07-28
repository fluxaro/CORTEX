"""Celery task for Repository IQ Engine & AI Intelligence execution."""

import asyncio
import logging
import uuid

from sqlalchemy import select

from app.analyzers.iq.engine import RepositoryIQEngine
from app.database.session import AsyncSessionLocal
from app.models.analysis import AnalysisRun, RepositoryMetrics
from app.models.architecture import ArchitectureAnalysis
from app.models.iq import (
    BenchmarkResult,
    EngineeringInsight,
    ExecutiveSummary,
    ImprovementRecommendation,
    RepositoryIQ,
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


async def _async_run_repository_iq(
    repository_id: str, run_id: str | None = None
) -> None:  # noqa: C901
    """Execute Repository IQ Engine pipeline."""
    repo_uuid = uuid.UUID(repository_id)
    async with AsyncSessionLocal() as session:
        # Load Repository
        r_stmt = select(Repository).where(Repository.id == repo_uuid)
        r_res = await session.execute(r_stmt)
        repo = r_res.scalar_one_or_none()
        if not repo:
            logger.error(
                f"Repository {repository_id} not found for Repository IQ analysis."
            )
            return

        logger.info(
            f"Repository IQ calculation started for repository {repo.full_name}"
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
                await session.flush()
                run_uuid = new_run.id

        # Load metrics from previous phases
        static_m = (
            await session.execute(
                select(RepositoryMetrics).where(
                    RepositoryMetrics.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        arch_m = (
            await session.execute(
                select(ArchitectureAnalysis).where(
                    ArchitectureAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        sec_m = (
            await session.execute(
                select(SecurityAnalysis).where(
                    SecurityAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        maint_m = (
            await session.execute(
                select(MaintainabilityMetrics).where(
                    MaintainabilityMetrics.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        doc_m = (
            await session.execute(
                select(DocumentationAnalysis).where(
                    DocumentationAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        test_m = (
            await session.execute(
                select(TestingAnalysis).where(
                    TestingAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        ci_m = (
            await session.execute(
                select(CiAnalysis).where(CiAnalysis.analysis_run_id == run_uuid)
            )
        ).scalar_one_or_none()

        git_m = (
            await session.execute(
                select(GitHistoryAnalysis).where(
                    GitHistoryAnalysis.analysis_run_id == run_uuid
                )
            )
        ).scalar_one_or_none()

        # Run Repository IQ Engine
        report = RepositoryIQEngine.run(
            repo_name=repo.name,
            static_metrics=static_m,
            arch_analysis=arch_m,
            sec_analysis=sec_m,
            maint_metrics=maint_m,
            doc_analysis=doc_m,
            test_analysis=test_m,
            ci_analysis=ci_m,
            git_history=git_m,
        )

        logger.info("Subsystem scores calculated")
        logger.info("AI provider selected")
        logger.info("Prompt executed")
        logger.info("Summary generated")
        logger.info("Recommendations generated")

        # Cleanup existing RepositoryIQ for this run_uuid if re-running
        old_iq = (
            await session.execute(
                select(RepositoryIQ).where(RepositoryIQ.analysis_run_id == run_uuid)
            )
        ).scalar_one_or_none()
        if old_iq:
            await session.delete(old_iq)
            await session.flush()

        # Persist RepositoryIQ Record
        iq_rec = RepositoryIQ(
            repository_id=repo_uuid,
            analysis_run_id=run_uuid,
            overall_score=report.overall_score,
            maturity_level=report.maturity.level,
            subsystem_scores={
                "static_analysis": report.subsystem_scores.static_analysis_score,
                "architecture": report.subsystem_scores.architecture_score,
                "security": report.subsystem_scores.security_score,
                "documentation": report.subsystem_scores.documentation_score,
                "testing": report.subsystem_scores.testing_score,
                "ci": report.subsystem_scores.ci_score,
                "git_practices": report.subsystem_scores.git_practices_score,
                "repository_health": report.subsystem_scores.repository_health_score,
                "community": report.subsystem_scores.community_score,
            },
        )
        session.add(iq_rec)
        await session.flush()

        # Persist Summaries
        session.add(
            RepositorySummary(
                repository_iq_id=iq_rec.id,
                executive_summary=report.executive_summary,
                technical_summary=report.technical_summary,
                architecture_summary=report.architecture_summary,
                security_summary=report.security_summary,
                maintainability_summary=report.maintainability_summary,
                recruiter_summary=report.recruiter_summary,
                engineering_manager_summary=report.engineering_manager_summary,
            )
        )

        # Persist Insights
        session.add(
            EngineeringInsight(
                repository_iq_id=iq_rec.id,
                strengths=report.insights.strengths,
                weaknesses=report.insights.weaknesses,
            )
        )

        # Persist Technical Debt
        session.add(
            TechnicalDebt(
                repository_iq_id=iq_rec.id,
                total_hours=report.debt.total_hours,
                total_days=report.debt.total_days,
                category_breakdown=report.debt.category_breakdown,
                items=[
                    {
                        "category": item.category,
                        "description": item.description,
                        "estimated_hours": item.estimated_hours,
                    }
                    for item in report.debt.items
                ],
            )
        )

        # Persist Recommendations
        for rec in report.insights.recommendations:
            session.add(
                ImprovementRecommendation(
                    repository_iq_id=iq_rec.id,
                    category=rec.category,
                    title=rec.title,
                    description=rec.description,
                    timeframe=rec.timeframe,
                    priority=rec.priority,
                    difficulty=rec.difficulty,
                    estimated_hours=rec.estimated_hours,
                )
            )

        # Persist Benchmark
        session.add(
            BenchmarkResult(
                repository_iq_id=iq_rec.id,
                overall_percentile=report.benchmark.overall_percentile,
                quality_percentile=report.benchmark.quality_percentile,
                security_percentile=report.benchmark.security_percentile,
                architecture_percentile=report.benchmark.architecture_percentile,
                maintainability_percentile=report.benchmark.maintainability_percentile,
            )
        )

        # Persist Executive & Technical Summaries JSON
        session.add(
            ExecutiveSummary(
                repository_iq_id=iq_rec.id,
                summary_text=report.executive_summary,
                report_json={
                    "overall_score": report.overall_score,
                    "maturity": report.maturity.level,
                },
            )
        )
        session.add(
            TechnicalSummary(
                repository_iq_id=iq_rec.id,
                summary_text=report.technical_summary,
                report_json={
                    "debt_hours": report.debt.total_hours,
                    "debt_days": report.debt.total_days,
                },
            )
        )

        await session.commit()
        logger.info("Persistence complete")
        logger.info(
            f"Repository IQ calculation completed for repository {repo.full_name}"
        )


@celery_app.task(name="app.tasks.repository_iq_tasks.repository_iq_task")
def repository_iq_task(repository_id: str, run_id: str | None = None) -> None:
    """Celery task entry point for Repository IQ calculation."""
    asyncio.run(_async_run_repository_iq(repository_id, run_id))
