"""Repository & Scan Version Comparison Service."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.enterprise import RepositoryComparison
from app.models.iq import RepositoryIQ
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
            select(Repository, RepositoryIQ)
            .outerjoin(RepositoryIQ, RepositoryIQ.repository_id == Repository.id)
            .where(Repository.id.in_(req.repository_ids))
        )

        res = await self.session.execute(stmt)
        rows = res.all()

        comparison_matrix: list[dict[str, Any]] = []
        for repo, iq in rows:
            comparison_matrix.append(
                {
                    "repository_id": repo.id,
                    "name": repo.name,
                    "overall_iq": iq.overall_score if iq else 0.0,
                    "security_score": iq.security_score if iq else 0.0,
                    "architecture_score": iq.architecture_score if iq else 0.0,
                    "maintainability_score": iq.static_analysis_score if iq else 0.0,
                    "debt_hours": iq.technical_debt_hours if iq else 0.0,
                    "maturity_level": iq.maturity_level if iq else "Unknown",
                }
            )

        comp = RepositoryComparison(
            workspace_id=req.workspace_id,
            title=req.title,
            repo_ids_json={"ids": req.repository_ids},
            comparison_data_json={"matrix": comparison_matrix},
        )
        self.session.add(comp)
        await self.session.commit()
        await self.session.refresh(comp)
        return comp
