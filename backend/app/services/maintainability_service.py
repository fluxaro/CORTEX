"""Maintainability & Repository Intelligence service layer."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analyzers.maintainability.engine import MaintainabilityEngine
from app.exceptions.custom_exceptions import RepositoryNotFoundError
from app.models.analysis import AnalysisRun
from app.models.maintainability import (
    CiAnalysis,
    CommitAnalysis,
    CommunityAnalysis,
    DocumentationAnalysis,
    GitHistoryAnalysis,
    LicenseAnalysis,
    MaintainabilityMetrics,
    ReadmeAnalysis,
    ReleaseAnalysis,
    RepositoryHealth,
    TestingAnalysis,
)
from app.models.repository import Repository


class MaintainabilityService:
    """Service handling Maintainability & Repository Intelligence analysis and querying."""

    @staticmethod
    async def trigger_maintainability_analysis(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> MaintainabilityMetrics:
        """Trigger synchronous Maintainability analysis for repository."""
        repo_res = await db.execute(
            select(Repository).where(Repository.id == repository_id)
        )
        repo = repo_res.scalar_one_or_none()
        if not repo or not repo.local_path:
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

        engine = MaintainabilityEngine(target_path=repo.local_path)
        report = engine.run()

        for model_cls in (
            DocumentationAnalysis,
            TestingAnalysis,
            GitHistoryAnalysis,
            ReleaseAnalysis,
            CommunityAnalysis,
            CiAnalysis,
            LicenseAnalysis,
            MaintainabilityMetrics,
            RepositoryHealth,
        ):
            old_stmt = select(model_cls).where(model_cls.analysis_run_id == run_id)
            old_res = await db.execute(old_stmt)
            old_obj = old_res.scalar_one_or_none()
            if old_obj:
                await db.delete(old_obj)
        await db.flush()

        m_record = MaintainabilityMetrics(
            repository_id=repository_id,
            analysis_run_id=run_id,
            documentation_score=report.documentation_score,
            testing_score=report.testing_score,
            ci_score=report.ci_score,
            release_score=report.release_score,
            repository_health_score=report.repository_health_score,
            community_score=report.community_score,
        )
        db.add(m_record)

        doc = report.documentation
        doc_rec = DocumentationAnalysis(
            repository_id=repository_id,
            analysis_run_id=run_id,
            documentation_score=doc.documentation_score,
            has_architecture_docs=doc.has_architecture_docs,
            has_api_docs=doc.has_api_docs,
            has_deployment_guide=doc.has_deployment_guide,
            has_dev_guide=doc.has_dev_guide,
            doc_frameworks=doc.doc_frameworks,
        )
        db.add(doc_rec)
        await db.flush()

        readme = doc.readme
        db.add(
            ReadmeAnalysis(
                repository_id=repository_id,
                documentation_analysis_id=doc_rec.id,
                completeness_percentage=readme.completeness_percentage,
                missing_sections=readme.missing_sections,
                detected_sections=readme.detected_sections,
                has_badges=readme.has_badges,
                has_screenshots=readme.has_screenshots,
            )
        )

        t = report.testing
        db.add(
            TestingAnalysis(
                repository_id=repository_id,
                analysis_run_id=run_id,
                testing_score=t.testing_score,
                frameworks=t.frameworks,
                test_file_count=t.test_file_count,
                estimated_test_count=t.estimated_test_count,
                has_unit_tests=t.has_unit_tests,
                has_integration_tests=t.has_integration_tests,
                has_e2e_tests=t.has_e2e_tests,
                has_mocks=t.has_mocks,
            )
        )

        ci = report.ci
        db.add(
            CiAnalysis(
                repository_id=repository_id,
                analysis_run_id=run_id,
                ci_score=ci.ci_score,
                providers=ci.providers,
                has_test_jobs=ci.has_test_jobs,
                has_lint_jobs=ci.has_lint_jobs,
                has_security_scans=ci.has_security_scans,
                has_build_jobs=ci.has_build_jobs,
                has_deploy_jobs=ci.has_deploy_jobs,
            )
        )

        gh = report.git_history
        gh_rec = GitHistoryAnalysis(
            repository_id=repository_id,
            analysis_run_id=run_id,
            commit_count=gh.commit_count,
            contributor_count=gh.contributor_count,
            branch_count=gh.branch_count,
            tag_count=gh.tag_count,
            repo_age_days=gh.repo_age_days,
            commits_per_week=gh.commits_per_week,
            inactive_periods_count=gh.inactive_periods_count,
            development_velocity_score=gh.development_velocity_score,
        )
        db.add(gh_rec)
        await db.flush()

        ca = report.commit_analysis
        db.add(
            CommitAnalysis(
                repository_id=repository_id,
                git_history_analysis_id=gh_rec.id,
                commit_quality_score=ca.commit_quality_score,
                conventional_commits_percentage=ca.conventional_commits_percentage,
                generic_commits_percentage=ca.generic_commits_percentage,
                commit_types_breakdown=ca.commit_types_breakdown,
            )
        )

        rel = report.release_analysis
        db.add(
            ReleaseAnalysis(
                repository_id=repository_id,
                analysis_run_id=run_id,
                release_score=rel.release_score,
                release_count=rel.release_count,
                has_changelog=rel.has_changelog,
                uses_semver=rel.uses_semver,
                latest_release_tag=rel.latest_release_tag,
                days_since_last_release=rel.days_since_last_release,
            )
        )

        comm = report.community
        db.add(
            CommunityAnalysis(
                repository_id=repository_id,
                analysis_run_id=run_id,
                community_score=comm.community_score,
                has_contributing=comm.has_contributing,
                has_code_of_conduct=comm.has_code_of_conduct,
                has_security_policy=comm.has_security_policy,
                has_issue_templates=comm.has_issue_templates,
                has_pr_templates=comm.has_pr_templates,
                has_discussions=comm.has_discussions,
            )
        )

        lic = report.license_analysis
        db.add(
            LicenseAnalysis(
                repository_id=repository_id,
                analysis_run_id=run_id,
                spdx_identifier=lic.spdx_identifier,
                is_osi_approved=lic.is_osi_approved,
                has_license_file=lic.has_license_file,
                is_consistent=lic.is_consistent,
            )
        )

        db.add(
            RepositoryHealth(
                repository_id=repository_id,
                analysis_run_id=run_id,
                repository_health_score=report.repository_health_score,
                maintenance_frequency_score=round(
                    min(gh.commits_per_week * 20.0, 100.0), 1
                ),
                community_readiness_score=comm.community_score,
                contribution_readiness_score=100.0 if comm.has_contributing else 50.0,
            )
        )

        await db.commit()
        return await MaintainabilityService.get_latest_maintainability(
            db, repository_id
        )

    @staticmethod
    async def get_latest_maintainability(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> MaintainabilityMetrics:
        """Get latest maintainability metrics for repository."""
        query = (
            select(MaintainabilityMetrics)
            .where(MaintainabilityMetrics.repository_id == repository_id)
            .order_by(MaintainabilityMetrics.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        m = res.scalar_one_or_none()
        if not m:
            raise RepositoryNotFoundError(
                identifier=f"Maintainability metrics for repository {repository_id}"
            )
        return m

    @staticmethod
    async def get_documentation(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> DocumentationAnalysis:
        """Get documentation analysis report."""
        query = (
            select(DocumentationAnalysis)
            .options(selectinload(DocumentationAnalysis.readme_analysis))
            .where(DocumentationAnalysis.repository_id == repository_id)
            .order_by(DocumentationAnalysis.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        doc = res.scalar_one_or_none()
        if not doc:
            raise RepositoryNotFoundError(
                identifier=f"Documentation analysis for repository {repository_id}"
            )
        return doc

    @staticmethod
    async def get_testing(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> TestingAnalysis:
        """Get testing analysis report."""
        query = (
            select(TestingAnalysis)
            .where(TestingAnalysis.repository_id == repository_id)
            .order_by(TestingAnalysis.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        t = res.scalar_one_or_none()
        if not t:
            raise RepositoryNotFoundError(
                identifier=f"Testing analysis for repository {repository_id}"
            )
        return t

    @staticmethod
    async def get_git_history(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> GitHistoryAnalysis:
        """Get Git history analysis report."""
        query = (
            select(GitHistoryAnalysis)
            .where(GitHistoryAnalysis.repository_id == repository_id)
            .order_by(GitHistoryAnalysis.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        gh = res.scalar_one_or_none()
        if not gh:
            raise RepositoryNotFoundError(
                identifier=f"Git history for repository {repository_id}"
            )
        return gh

    @staticmethod
    async def get_commits(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> CommitAnalysis:
        """Get commit quality analysis report."""
        query = (
            select(CommitAnalysis)
            .where(CommitAnalysis.repository_id == repository_id)
            .order_by(CommitAnalysis.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        ca = res.scalar_one_or_none()
        if not ca:
            raise RepositoryNotFoundError(
                identifier=f"Commit analysis for repository {repository_id}"
            )
        return ca

    @staticmethod
    async def get_releases(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> ReleaseAnalysis:
        """Get release analysis report."""
        query = (
            select(ReleaseAnalysis)
            .where(ReleaseAnalysis.repository_id == repository_id)
            .order_by(ReleaseAnalysis.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        rel = res.scalar_one_or_none()
        if not rel:
            raise RepositoryNotFoundError(
                identifier=f"Release analysis for repository {repository_id}"
            )
        return rel

    @staticmethod
    async def get_ci(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> CiAnalysis:
        """Get CI/CD analysis report."""
        query = (
            select(CiAnalysis)
            .where(CiAnalysis.repository_id == repository_id)
            .order_by(CiAnalysis.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        ci = res.scalar_one_or_none()
        if not ci:
            raise RepositoryNotFoundError(
                identifier=f"CI analysis for repository {repository_id}"
            )
        return ci

    @staticmethod
    async def get_community(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> CommunityAnalysis:
        """Get community standards analysis report."""
        query = (
            select(CommunityAnalysis)
            .where(CommunityAnalysis.repository_id == repository_id)
            .order_by(CommunityAnalysis.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        comm = res.scalar_one_or_none()
        if not comm:
            raise RepositoryNotFoundError(
                identifier=f"Community analysis for repository {repository_id}"
            )
        return comm

    @staticmethod
    async def get_repository_health(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> RepositoryHealth:
        """Get repository health report."""
        query = (
            select(RepositoryHealth)
            .where(RepositoryHealth.repository_id == repository_id)
            .order_by(RepositoryHealth.id.desc())
            .limit(1)
        )
        res = await db.execute(query)
        rh = res.scalar_one_or_none()
        if not rh:
            raise RepositoryNotFoundError(
                identifier=f"Repository health for repository {repository_id}"
            )
        return rh
