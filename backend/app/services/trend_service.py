"""Trend Analysis service for time-series metrics."""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import TrendMetric
from app.models.iq import RepositoryIQ


class TrendService:
    """Service managing historical time-series trends."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def record_snapshot(
        self, repository_id: str, iq_report: RepositoryIQ
    ) -> TrendMetric:
        """Record a time-series metric snapshot."""
        scores = iq_report.subsystem_scores or {}
        debt_hrs = (
            iq_report.technical_debt.total_hours if iq_report.technical_debt else 0.0
        )
        trend = TrendMetric(
            repository_id=repository_id,
            recorded_at=datetime.utcnow(),
            overall_iq=iq_report.overall_score,
            security_score=float(scores.get("security", 0.0)),
            architecture_score=float(scores.get("architecture", 0.0)),
            complexity_score=float(scores.get("static_analysis", 0.0)),
            documentation_score=float(scores.get("documentation", 0.0)),
            debt_hours=float(debt_hrs),
            testing_score=float(scores.get("testing", 0.0)),
        )
        self.session.add(trend)
        await self.session.commit()
        await self.session.refresh(trend)
        return trend

    async def get_repository_trends(
        self, repository_id: str, limit: int = 30
    ) -> list[TrendMetric]:
        """Fetch chronological trend metrics for a repository."""
        stmt = (
            select(TrendMetric)
            .where(TrendMetric.repository_id == repository_id)
            .order_by(TrendMetric.recorded_at.asc())
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
