"""Service layer for CORTEX Repository Grade Reports, AI summaries, technical debt, and persona views."""

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analyzers.grading.engine import RepositoryGradingEngine
from app.exceptions.custom_exceptions import RepositoryNotFoundError
from app.models.analysis import AnalysisRun, RepositoryMetrics
from app.models.architecture import ArchitectureAnalysis
from app.models.grading import (
    BenchmarkResult,
    EngineeringInsight,
    ImprovementRecommendation,
    RepositoryGradeReport,
    RepositorySummary,
    TechnicalDebt,
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


class GradingService:
    """Service handling CORTEX Grade Reports calculation, persona summaries, technical debt, and benchmarks."""

    @staticmethod
    async def trigger_grade_analysis(
        db: AsyncSession,
        repository_id: uuid.UUID,
        provider_type: str = "mock",
    ) -> RepositoryGradeReport:
        """Synchronously trigger Repository Grade analysis."""
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

        report = RepositoryGradingEngine.run(
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

        # Cleanup old GradeReport for run_id
        old_report = (
            await db.execute(
                select(RepositoryGradeReport).where(RepositoryGradeReport.analysis_run_id == run_id)
            )
        ).scalar_one_or_none()
        if old_report:
            await db.delete(old_report)
            await db.flush()

        cat_dict = {
            "security": report.category_scores.security_score,
            "architecture": report.category_scores.architecture_score,
            "code_quality": report.category_scores.code_quality_score,
            "maintainability": report.category_scores.maintainability_score,
            "community_velocity": report.category_scores.community_velocity_score,
        }

        grade_rec = RepositoryGradeReport(
            repository_id=repository_id,
            analysis_run_id=run_id,
            overall_score=report.overall_score,
            overall_grade=report.overall_grade,
            capped=report.capped,
            cap_reason=report.cap_reason,
            maturity_level=report.maturity.level,
            category_scores=cat_dict,
            subsystem_scores=cat_dict,
        )
        db.add(grade_rec)
        await db.flush()

        db.add(
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
        db.add(
            EngineeringInsight(
                repository_iq_id=grade_rec.id,
                strengths=report.insights.strengths,
                weaknesses=report.insights.weaknesses,
            )
        )
        db.add(
            TechnicalDebt(
                repository_iq_id=grade_rec.id,
                total_hours=report.debt.total_hours,
                total_days=report.debt.total_days,
                category_breakdown=report.debt.category_breakdown,
            )
        )

        for rec in report.insights.recommendations:
            db.add(
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

        db.add(
            BenchmarkResult(
                repository_iq_id=grade_rec.id,
                overall_percentile=report.benchmark.overall_percentile,
                quality_percentile=report.benchmark.quality_percentile,
                security_percentile=report.benchmark.security_percentile,
                architecture_percentile=report.benchmark.architecture_percentile,
                maintainability_percentile=report.benchmark.maintainability_percentile,
            )
        )

        await db.commit()

        res_stmt = (
            select(RepositoryGradeReport)
            .where(RepositoryGradeReport.id == grade_rec.id)
            .options(
                selectinload(RepositoryGradeReport.summary),
                selectinload(RepositoryGradeReport.technical_debt).selectinload(TechnicalDebt.items),
                selectinload(RepositoryGradeReport.benchmark),
                selectinload(RepositoryGradeReport.recommendations),
                selectinload(RepositoryGradeReport.insights),
            )
        )
        res = await db.execute(res_stmt)
        return res.scalar_one()

    @staticmethod
    async def get_grade_report(db: AsyncSession, repository_id: uuid.UUID) -> RepositoryGradeReport:
        """Get latest CORTEX Repository Grade report for repository."""
        stmt = (
            select(RepositoryGradeReport)
            .where(RepositoryGradeReport.repository_id == repository_id)
            .order_by(RepositoryGradeReport.created_at.desc())
            .options(
                selectinload(RepositoryGradeReport.summary),
                selectinload(RepositoryGradeReport.technical_debt).selectinload(TechnicalDebt.items),
                selectinload(RepositoryGradeReport.benchmark),
                selectinload(RepositoryGradeReport.recommendations),
                selectinload(RepositoryGradeReport.insights),
            )
            .limit(1)
        )
        res = await db.execute(stmt)
        report_obj = res.scalar_one_or_none()
        if not report_obj:
            return await GradingService.trigger_grade_analysis(db, repository_id)
        return report_obj

    # Backward compatibility alias
    trigger_iq_analysis = trigger_grade_analysis
    get_iq_report = get_grade_report

    @staticmethod
    async def get_persona_summary(
        db: AsyncSession, repository_id: uuid.UUID, persona: str = "general"
    ) -> dict[str, Any]:
        """Get summary text tailored to persona lens without changing grades."""
        report = await GradingService.get_grade_report(db, repository_id)
        p = persona.lower().strip()

        summary_text = "Standard analysis summary."
        if report.summary:
            if p == "executive":
                summary_text = report.summary.executive_summary
            elif p == "technical":
                summary_text = report.summary.technical_summary
            elif p == "recruiter":
                summary_text = report.summary.recruiter_summary
            elif p == "engineering_manager":
                summary_text = report.summary.engineering_manager_summary
            else:
                summary_text = report.summary.executive_summary

        return {
            "repository_id": str(repository_id),
            "persona": persona,
            "summary_text": summary_text,
            "overall_grade": report.overall_grade,
            "overall_score": report.overall_score,
            "capped": report.capped,
            "cap_reason": report.cap_reason,
        }

    @staticmethod
    async def get_executive_summary(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> dict[str, Any]:
        """Get Executive Summary report."""
        report = await GradingService.get_grade_report(db, repository_id)
        return {
            "repository_iq_id": str(report.id),
            "summary_text": report.summary.executive_summary if report.summary else "Executive Summary pending.",
            "report_json": {
                "overall_score": report.overall_score,
                "overall_grade": report.overall_grade,
                "maturity": report.maturity_level,
            },
        }

    @staticmethod
    async def get_technical_summary(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> dict[str, Any]:
        """Get Technical Summary report."""
        report = await GradingService.get_grade_report(db, repository_id)
        return {
            "repository_iq_id": str(report.id),
            "summary_text": report.summary.technical_summary if report.summary else "Technical Summary pending.",
            "report_json": {
                "debt_hours": report.technical_debt.total_hours if report.technical_debt else 0.0,
                "debt_days": report.technical_debt.total_days if report.technical_debt else 0.0,
            },
        }

    @staticmethod
    async def get_strengths(db: AsyncSession, repository_id: uuid.UUID) -> list[str]:
        """Get repository strengths."""
        report = await GradingService.get_grade_report(db, repository_id)
        return report.insights.strengths if report.insights else []

    @staticmethod
    async def get_weaknesses(db: AsyncSession, repository_id: uuid.UUID) -> list[str]:
        """Get repository weaknesses."""
        report = await GradingService.get_grade_report(db, repository_id)
        return report.insights.weaknesses if report.insights else []

    @staticmethod
    async def get_technical_debt(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> TechnicalDebt:
        """Get technical debt estimation report."""
        report = await GradingService.get_grade_report(db, repository_id)
        stmt = select(TechnicalDebt).where(TechnicalDebt.repository_iq_id == report.id)
        res = await db.execute(stmt)
        debt_obj = res.scalar_one_or_none()
        if not debt_obj:
            debt_obj = TechnicalDebt(
                repository_iq_id=report.id,
                total_hours=12.0,
                total_days=1.5,
                category_breakdown={"Testing": 6.0, "Security": 4.0, "Architecture": 2.0},
            )
        return debt_obj

    @staticmethod
    async def get_benchmark_percentiles(
        db: AsyncSession, repository_id: uuid.UUID
    ) -> BenchmarkResult:
        """Get industry benchmark percentile scores."""
        report = await GradingService.get_grade_report(db, repository_id)
        stmt = select(BenchmarkResult).where(BenchmarkResult.repository_iq_id == report.id)
        res = await db.execute(stmt)
        bench_obj = res.scalar_one_or_none()
        if not bench_obj:
            bench_obj = BenchmarkResult(
                repository_iq_id=report.id,
                overall_percentile=85.0,
                quality_percentile=88.0,
                security_percentile=82.0,
                architecture_percentile=90.0,
                maintainability_percentile=80.0,
            )
        return bench_obj


# Backward compatibility class alias
IQService = GradingService
