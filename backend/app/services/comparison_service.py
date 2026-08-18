"""Repository & Scan Version Comparison Service."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import RepositoryComparison
from app.models.grading import RepositoryGradeReport, RepositoryIQ
from app.models.repository import Repository
from app.schemas.enterprise import RepositoryComparisonRequest


class ComparisonService:
    """Service comparing multiple repositories or scan versions."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def compare_repositories(
        self, req: RepositoryComparisonRequest
    ) -> RepositoryComparison:
        """Compare scores and findings across multiple repositories."""
        stmt = (
            select(Repository, RepositoryGradeReport)
            .join(
                RepositoryGradeReport, Repository.id == RepositoryGradeReport.repository_id
            )
            .where(Repository.id.in_(req.repository_ids))
        )
        res = await self.session.execute(stmt)
        rows = res.all()

        matrix: dict[str, Any] = {}
        for repo, report in rows:
            matrix[str(repo.id)] = {
                "name": repo.name,
                "overall_score": report.overall_score,
                "overall_grade": getattr(report, "overall_grade", "C"),
                "capped": getattr(report, "capped", False),
                "cap_reason": getattr(report, "cap_reason", None),
                "maturity": report.maturity_level,
                "category_scores": report.category_scores,
            }

        comparison = RepositoryComparison(
            workspace_id=req.workspace_id,
            name=req.name,
            comparison_matrix=matrix,
        )
        self.session.add(comparison)
        await self.session.commit()
        await self.session.refresh(comparison)
        return comparison
