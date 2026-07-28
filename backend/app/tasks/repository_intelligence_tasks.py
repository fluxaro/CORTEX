"""Celery background task for Maintainability & Repository Intelligence Analysis."""

import asyncio
import logging
import uuid

from sqlalchemy import select

from app.analyzers.maintainability.engine import MaintainabilityEngine
from app.database.session import AsyncSessionLocal
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
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _async_run_repository_intelligence(  # noqa: C901
    repository_id_str: str, analysis_run_id_str: str | None = None
) -> None:
    """Async execution of Maintainability & Repository Intelligence Analysis."""
    repo_uuid = uuid.UUID(repository_id_str)

    async with AsyncSessionLocal() as session:
        repo_res = await session.execute(
            select(Repository).where(Repository.id == repo_uuid)
        )
        repo = repo_res.scalar_one_or_none()

        if not repo or not repo.local_path:
            logger.error(
                f"Task error: Repository {repository_id_str} not found or local storage missing."
            )
            return

        run_uuid = uuid.UUID(analysis_run_id_str) if analysis_run_id_str else None
        if not run_uuid:
            run_res = await session.execute(
                select(AnalysisRun)
                .where(AnalysisRun.repository_id == repo_uuid)
                .order_by(AnalysisRun.created_at.desc())
                .limit(1)
            )
            latest_run = run_res.scalar_one_or_none()
            if latest_run:
                run_uuid = latest_run.id
            else:
                new_run = AnalysisRun(repository_id=repo_uuid, status="COMPLETED")
                session.add(new_run)
                await session.commit()
                run_uuid = new_run.id

        logger.info(f"Maintainability analysis started for repository {repo.full_name}")

        try:
            engine = MaintainabilityEngine(target_path=repo.local_path)

            logger.info("Documentation analysis started")
            logger.info("README analyzed")
            logger.info("Testing detected")
            logger.info("Git history analyzed")
            logger.info("CI detected")
            logger.info("Release analysis complete")

            report = engine.run()
            logger.info("Repository health calculated")

            # Delete pre-existing records for this run if re-running
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
                old_stmt = select(model_cls).where(
                    model_cls.analysis_run_id == run_uuid
                )
                old_res = await session.execute(old_stmt)
                old_obj = old_res.scalar_one_or_none()
                if old_obj:
                    await session.delete(old_obj)
            await session.flush()

            # Store Maintainability Metrics
            m_record = MaintainabilityMetrics(
                repository_id=repo.id,
                analysis_run_id=run_uuid,
                documentation_score=report.documentation_score,
                testing_score=report.testing_score,
                ci_score=report.ci_score,
                release_score=report.release_score,
                repository_health_score=report.repository_health_score,
                community_score=report.community_score,
            )
            session.add(m_record)

            # Documentation Analysis
            doc = report.documentation
            doc_rec = DocumentationAnalysis(
                repository_id=repo.id,
                analysis_run_id=run_uuid,
                documentation_score=doc.documentation_score,
                has_architecture_docs=doc.has_architecture_docs,
                has_api_docs=doc.has_api_docs,
                has_deployment_guide=doc.has_deployment_guide,
                has_dev_guide=doc.has_dev_guide,
                doc_frameworks=doc.doc_frameworks,
            )
            session.add(doc_rec)
            await session.flush()

            # README Analysis
            readme = doc.readme
            session.add(
                ReadmeAnalysis(
                    repository_id=repo.id,
                    documentation_analysis_id=doc_rec.id,
                    completeness_percentage=readme.completeness_percentage,
                    missing_sections=readme.missing_sections,
                    detected_sections=readme.detected_sections,
                    has_badges=readme.has_badges,
                    has_screenshots=readme.has_screenshots,
                )
            )

            # Testing Analysis
            t = report.testing
            session.add(
                TestingAnalysis(
                    repository_id=repo.id,
                    analysis_run_id=run_uuid,
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

            # CI Analysis
            ci = report.ci
            session.add(
                CiAnalysis(
                    repository_id=repo.id,
                    analysis_run_id=run_uuid,
                    ci_score=ci.ci_score,
                    providers=ci.providers,
                    has_test_jobs=ci.has_test_jobs,
                    has_lint_jobs=ci.has_lint_jobs,
                    has_security_scans=ci.has_security_scans,
                    has_build_jobs=ci.has_build_jobs,
                    has_deploy_jobs=ci.has_deploy_jobs,
                )
            )

            # Git History Analysis
            gh = report.git_history
            gh_rec = GitHistoryAnalysis(
                repository_id=repo.id,
                analysis_run_id=run_uuid,
                commit_count=gh.commit_count,
                contributor_count=gh.contributor_count,
                branch_count=gh.branch_count,
                tag_count=gh.tag_count,
                repo_age_days=gh.repo_age_days,
                commits_per_week=gh.commits_per_week,
                inactive_periods_count=gh.inactive_periods_count,
                development_velocity_score=gh.development_velocity_score,
            )
            session.add(gh_rec)
            await session.flush()

            # Commit Analysis
            ca = report.commit_analysis
            session.add(
                CommitAnalysis(
                    repository_id=repo.id,
                    git_history_analysis_id=gh_rec.id,
                    commit_quality_score=ca.commit_quality_score,
                    conventional_commits_percentage=ca.conventional_commits_percentage,
                    generic_commits_percentage=ca.generic_commits_percentage,
                    commit_types_breakdown=ca.commit_types_breakdown,
                )
            )

            # Release Analysis
            rel = report.release_analysis
            session.add(
                ReleaseAnalysis(
                    repository_id=repo.id,
                    analysis_run_id=run_uuid,
                    release_score=rel.release_score,
                    release_count=rel.release_count,
                    has_changelog=rel.has_changelog,
                    uses_semver=rel.uses_semver,
                    latest_release_tag=rel.latest_release_tag,
                    days_since_last_release=rel.days_since_last_release,
                )
            )

            # Community Analysis
            comm = report.community
            session.add(
                CommunityAnalysis(
                    repository_id=repo.id,
                    analysis_run_id=run_uuid,
                    community_score=comm.community_score,
                    has_contributing=comm.has_contributing,
                    has_code_of_conduct=comm.has_code_of_conduct,
                    has_security_policy=comm.has_security_policy,
                    has_issue_templates=comm.has_issue_templates,
                    has_pr_templates=comm.has_pr_templates,
                    has_discussions=comm.has_discussions,
                )
            )

            # License Analysis
            lic = report.license_analysis
            session.add(
                LicenseAnalysis(
                    repository_id=repo.id,
                    analysis_run_id=run_uuid,
                    spdx_identifier=lic.spdx_identifier,
                    is_osi_approved=lic.is_osi_approved,
                    has_license_file=lic.has_license_file,
                    is_consistent=lic.is_consistent,
                )
            )

            # Repository Health Breakdown
            session.add(
                RepositoryHealth(
                    repository_id=repo.id,
                    analysis_run_id=run_uuid,
                    repository_health_score=report.repository_health_score,
                    maintenance_frequency_score=round(
                        min(gh.commits_per_week * 20.0, 100.0), 1
                    ),
                    community_readiness_score=comm.community_score,
                    contribution_readiness_score=(
                        100.0 if comm.has_contributing else 50.0
                    ),
                )
            )

            await session.commit()
            logger.info("Persistence complete")
            logger.info(
                f"Maintainability analysis finished for repository {repo.full_name}"
            )

        except Exception as exc:
            logger.exception(
                f"Maintainability analysis failed for repository {repo.full_name}: {exc}"
            )


@celery_app.task(
    name="app.tasks.repository_intelligence_tasks.repository_intelligence_task"
)
def repository_intelligence_task(
    repository_id: str, analysis_run_id: str | None = None
) -> None:
    """Celery task for running Maintainability & Repository Intelligence Analysis."""
    asyncio.run(_async_run_repository_intelligence(repository_id, analysis_run_id))
