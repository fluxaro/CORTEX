"""Service layer for Repository IQ Engine, summaries, technical debt, and recommendations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analyzers.iq.engine import RepositoryIQEngine
from app.exceptions.custom_exceptions import RepositoryNotFoundError
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


class IQService:
    """Service handling Repository IQ calculation, queries, summaries, technical debt, recommendations, and benchmark."""

    @staticmethod
    async def trigger_iq_analysis(
        db: AsyncSession,
        repository_id: uuid.UUID,
        provider_type: str = "mock",
    ) -> RepositoryIQ:
        """Synchronously trigger Repository IQ analysis."""
        repo_res = await db.execute(
            select(Repository).where(Repository.id == repository_id)
        )
        repo = repo_res.scalar_one_or_none()
        if not repo:
            raise RepositoryNotFoundError(identifier=str(repository_id))

        run_res = await db.execute(
            select(AnalysisRun)
            .where(AnalysisRun.repository_id == repository_id)
            .order_by(AnalysisRun.created_at.desc())
            .limit(1)
        )
        latest_run = run_res.scalar_one_or_none()
        if latest_run:
            run_id = latest_run.id
        else:
            new_run = AnalysisRun(repository_id=repository_id, status="COMPLETED")
            db.add(new_run)
            await db.commit()
            run_id = new_run.id

        # Load existing metrics
        static_m = (
            await db.execute(
                select(RepositoryMetrics).where(
                    RepositoryMetrics.analysis_run_id == run_id
                )
            )
        ).scalar_one_or_none()
        arch_m = (
            await db.execute(
                select(ArchitectureAnalysis).where(
                    ArchitectureAnalysis.analysis_run_id == run_id
                )
            )
        ).scalar_one_or_none()
        sec_m = (
            await db.execute(
                select(SecurityAnalysis).where(
                    SecurityAnalysis.analysis_run_id == run_id
                )
            )
        ).scalar_one_or_none()
        maint_m = (
            await db.execute(
                select(MaintainabilityMetrics).where(
                    MaintainabilityMetrics.analysis_run_id == run_id
                )
            )
        ).scalar_one_or_none()
        doc_m = (
            await db.execute(
                select(DocumentationAnalysis).where(
                    DocumentationAnalysis.analysis_run_id == run_id
                )
            )
        ).scalar_one_or_none()
        test_m = (
            await db.execute(
                select(TestingAnalysis).where(TestingAnalysis.analysis_run_id == run_id)
            )
        ).scalar_one_or_none()
        ci_m = (
            await db.execute(
                select(CiAnalysis).where(CiAnalysis.analysis_run_id == run_id)
            )
        ).scalar_one_or_none()
        git_m = (
            await db.execute(
                select(GitHistoryAnalysis).where(
                    GitHistoryAnalysis.analysis_run_id == run_id
                )
            )
        ).scalar_one_or_none()

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
            provider_type=provider_type,
        )

        # Cleanup old RepositoryIQ for run_id
        old_iq = (
            await db.execute(
                select(RepositoryIQ).where(RepositoryIQ.analysis_run_id == run_id)
            )
        ).scalar_one_or_none()
        if old_iq:
            await db.delete(old_iq)
            await db.flush()

        iq_rec = RepositoryIQ(
            repository_id=repository_id,
            analysis_run_id=run_id,
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
        db.add(iq_rec)
        await db.flush()

        db.add(
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
        db.add(
            EngineeringInsight(
                repository_iq_id=iq_rec.id,
                strengths=report.insights.strengths,
                weaknesses=report.insights.weaknesses,
            )
        )
        db.add(
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

        for rec in report.insights.recommendations:
            db.add(
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

        db.add(
            BenchmarkResult(
                repository_iq_id=iq_rec.id,
                overall_percentile=report.benchmark.overall_percentile,
                quality_percentile=report.benchmark.quality_percentile,
                security_percentile=report.benchmark.security_percentile,
                architecture_percentile=report.benchmark.architecture_percentile,
                maintainability_percentile=report.benchmark.maintainability_percentile,
            )
        )
        db.add(
            ExecutiveSummary(
                repository_iq_id=iq_rec.id,
                summary_text=report.executive_summary,
                report_json={
                    "overall_score": report.overall_score,
                    "maturity": report.maturity.level,
                },
            )
        )
        db.add(
            TechnicalSummary(
                repository_iq_id=iq_rec.id,
                summary_text=report.technical_summary,
                report_json={
                    "debt_hours": report.debt.total_hours,
                    "debt_days": report.debt.total_days,
                },
            )
        )

        await db.commit()

        res_stmt = (
            select(RepositoryIQ)
            .where(RepositoryIQ.id == iq_rec.id)
            .options(
                selectinload(RepositoryIQ.summary),
                selectinload(RepositoryIQ.technical_debt),
                selectinload(RepositoryIQ.benchmark),
                selectinload(RepositoryIQ.recommendations),
                selectinload(RepositoryIQ.insights),
            )
        )
        res = await db.execute(res_stmt)
        return res.scalar_one()

    @staticmethod
    async def get_iq_report(db: AsyncSession, repository_id: uuid.UUID) -> RepositoryIQ:
        """Get latest Repository IQ report for repository."""
        stmt = (
            select(RepositoryIQ)
            .where(RepositoryIQ.repository_id == repository_id)
            .order_by(RepositoryIQ.created_at.desc())
            .options(
                selectinload(RepositoryIQ.summary),
                selectinload(RepositoryIQ.technical_debt),
                selectinload(RepositoryIQ.benchmark),
                selectinload(RepositoryIQ.recommendations),
                selectinload(RepositoryIQ.insights),
            )
            .limit(1)
        )
        res = await db.execute(stmt)
        iq_obj = res.scalar_one_or_none()
        if not iq_obj:
            return await IQService.trigger_iq_analysis(db, repository_id)
        return iq_obj

    @staticmethod
    async def get_executive_summary(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> ExecutiveSummary:
        """Get Executive Summary report."""
        iq_obj = await IQService.get_iq_report(db, repository_id)
        stmt = select(ExecutiveSummary).where(
            ExecutiveSummary.repository_iq_id == iq_obj.id
        )
        res = await db.execute(stmt)
        exec_obj = res.scalar_one_or_none()
        if not exec_obj:
            exec_obj = ExecutiveSummary(
                repository_iq_id=iq_obj.id,
                summary_text=(
                    iq_obj.summary.executive_summary
                    if iq_obj.summary
                    else "Executive Summary pending."
                ),
                report_json={
                    "overall_score": iq_obj.overall_score,
                    "maturity": iq_obj.maturity_level,
                },
            )
            db.add(exec_obj)
            await db.commit()
        return exec_obj

    @staticmethod
    async def get_technical_summary(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> TechnicalSummary:
        """Get Technical Summary report."""
        iq_obj = await IQService.get_iq_report(db, repository_id)
        stmt = select(TechnicalSummary).where(
            TechnicalSummary.repository_iq_id == iq_obj.id
        )
        res = await db.execute(stmt)
        tech_obj = res.scalar_one_or_none()
        if not tech_obj:
            tech_obj = TechnicalSummary(
                repository_iq_id=iq_obj.id,
                summary_text=(
                    iq_obj.summary.technical_summary
                    if iq_obj.summary
                    else "Technical Summary pending."
                ),
                report_json={
                    "debt_hours": (
                        iq_obj.technical_debt.total_hours
                        if iq_obj.technical_debt
                        else 0.0
                    ),
                    "debt_days": (
                        iq_obj.technical_debt.total_days
                        if iq_obj.technical_debt
                        else 0.0
                    ),
                },
            )
            db.add(tech_obj)
            await db.commit()
        return tech_obj

    @staticmethod
    async def get_strengths(db: AsyncSession, repository_id: uuid.UUID) -> list[str]:
        """Get repository strengths."""
        iq_obj = await IQService.get_iq_report(db, repository_id)
        return iq_obj.insights.strengths if iq_obj.insights else []

    @staticmethod
    async def get_weaknesses(db: AsyncSession, repository_id: uuid.UUID) -> list[str]:
        """Get repository weaknesses."""
        iq_obj = await IQService.get_iq_report(db, repository_id)
        return iq_obj.insights.weaknesses if iq_obj.insights else []

    @staticmethod
    async def get_technical_debt(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> TechnicalDebt:
        """Get technical debt estimation report."""
        iq_obj = await IQService.get_iq_report(db, repository_id)
        stmt = select(TechnicalDebt).where(TechnicalDebt.repository_iq_id == iq_obj.id)
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def get_recommendations(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        category: str | None = None,
        priority: str | None = None,
    ) -> tuple[list[ImprovementRecommendation], int]:
        """Get paginated improvement recommendations."""
        iq_obj = await IQService.get_iq_report(db, repository_id)
        query = select(ImprovementRecommendation).where(
            ImprovementRecommendation.repository_iq_id == iq_obj.id
        )

        if category:
            query = query.where(
                ImprovementRecommendation.category.ilike(f"%{category}%")
            )
        if priority:
            query = query.where(
                ImprovementRecommendation.priority.ilike(f"%{priority}%")
            )

        count_res = await db.execute(query)
        total = len(count_res.scalars().all())

        offset = (page - 1) * page_size
        items_res = await db.execute(query.offset(offset).limit(page_size))
        items = items_res.scalars().all()
        return list(items), total

    @staticmethod
    async def get_benchmark(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> BenchmarkResult:
        """Get industry benchmark percentile scores."""
        iq_obj = await IQService.get_iq_report(db, repository_id)
        stmt = select(BenchmarkResult).where(
            BenchmarkResult.repository_iq_id == iq_obj.id
        )
        res = await db.execute(stmt)
        return res.scalar_one()
