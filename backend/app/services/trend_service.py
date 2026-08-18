"""Trend Analysis service for time-series metrics."""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import TrendMetric
from app.models.grading import RepositoryGradeReport, RepositoryIQ


class TrendService:
    """Service managing historical time-series trends."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def record_snapshot(
        self, repository_id: str, grade_report: RepositoryGradeReport
    ) -> TrendMetric:
        """Record a time-series metric snapshot."""
        scores = grade_report.category_scores or grade_report.subsystem_scores or {}
        debt_hrs = (
            grade_report.technical_debt.total_hours if grade_report.technical_debt else 0.0
        )

        trend = TrendMetric(
            repository_id=repository_id,
            recorded_at=datetime.utcnow(),
            overall_score=grade_report.overall_score,
            overall_grade=getattr(grade_report, "overall_grade", "C"),
            security_score=scores.get("security", 0.0),
            architecture_score=scores.get("architecture", 0.0),
            code_quality_score=scores.get("code_quality", scores.get("static_analysis", 0.0)),
            maintainability_score=scores.get("maintainability", 0.0),
            debt_hours=debt_hrs,
        )
        self.session.add(trend)
        await self.session.commit()
        await self.session.refresh(trend)
        return trend

    async def get_trends(
        self, repository_id: str, limit: int = 30
    ) -> list[TrendMetric]:
        """Fetch historical trends for a repository."""
        stmt = (
            select(TrendMetric)
            .where(TrendMetric.repository_id == repository_id)
            .order_by(TrendMetric.recorded_at.asc())
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
