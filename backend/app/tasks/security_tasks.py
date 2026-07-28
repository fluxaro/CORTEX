"""Celery background task for running Security Intelligence Analysis."""

import asyncio
import logging
import uuid

from sqlalchemy import select

from app.analyzers.security.engine import SecurityIntelligenceEngine
from app.database.session import AsyncSessionLocal
from app.models.analysis import AnalysisRun
from app.models.repository import Repository
from app.models.security import (
    AuthenticationFinding,
    AuthorizationFinding,
    ConfigurationFinding,
    DependencyFinding,
    SecretFinding,
    SecurityAnalysis,
    SecurityFinding,
)
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _async_run_security_analysis(  # noqa: C901
    repository_id_str: str, analysis_run_id_str: str | None = None
) -> None:
    """Async execution of Security Intelligence Analysis (SAST)."""
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

        logger.info(
            f"Security analysis started for repository {repo.full_name} (Run ID: {run_uuid})"
        )

        try:
            logger.info("Load Static Analysis")
            engine = SecurityIntelligenceEngine(target_path=repo.local_path)

            logger.info("Run Secret Detection")
            logger.info("Run Configuration Scan")
            logger.info("Run Dependency Scan")
            logger.info("Run Security Rules")

            report = engine.run()

            # Delete pre-existing security analysis for this run if re-running
            existing_sec = await session.execute(
                select(SecurityAnalysis).where(
                    SecurityAnalysis.analysis_run_id == run_uuid
                )
            )
            old_sec = existing_sec.scalar_one_or_none()
            if old_sec:
                await session.delete(old_sec)
                await session.flush()

            logger.info("Persist Findings")
            sec_record = SecurityAnalysis(
                repository_id=repo.id,
                analysis_run_id=run_uuid,
                critical_count=report.critical_count,
                high_count=report.high_count,
                medium_count=report.medium_count,
                low_count=report.low_count,
                info_count=report.info_count,
                secret_count=report.secret_count,
                dependency_vuln_count=report.dependency_vuln_count,
                config_issues_count=report.config_issues_count,
                auth_issues_count=report.auth_issues_count,
            )
            session.add(sec_record)
            await session.flush()

            # Store Findings
            for f_res in report.findings:
                session.add(
                    SecurityFinding(
                        security_analysis_id=sec_record.id,
                        repository_id=repo.id,
                        rule_id=f_res.rule_id,
                        rule_name=f_res.rule_name,
                        category=f_res.category,
                        severity=f_res.severity,
                        confidence=f_res.confidence,
                        language=f_res.language,
                        file_path=f_res.file_path,
                        line_number=f_res.line_number,
                        column_number=f_res.column_number,
                        description=f_res.description,
                        remediation_placeholder=f_res.remediation_placeholder,
                        reference_url=f_res.reference_url,
                        cvss_score=f_res.cvss_score,
                    )
                )

            # Store Secrets
            for s_res in report.secrets:
                session.add(
                    SecretFinding(
                        security_analysis_id=sec_record.id,
                        repository_id=repo.id,
                        secret_type=s_res.secret_type,
                        severity=s_res.severity,
                        line_number=s_res.line_number,
                        file_path=s_res.file_path,
                        entropy=s_res.entropy,
                        masked_value=s_res.masked_value,
                        description=s_res.description,
                    )
                )

            # Store Dependencies
            for d_res in report.dependencies:
                session.add(
                    DependencyFinding(
                        security_analysis_id=sec_record.id,
                        repository_id=repo.id,
                        package_name=d_res.package_name,
                        version=d_res.version,
                        cve_id=d_res.cve_id,
                        cvss_score=d_res.cvss_score,
                        severity=d_res.severity,
                        license=d_res.license,
                        description=d_res.description,
                        references=d_res.references,
                    )
                )

            # Store Configurations
            for c_res in report.configs:
                session.add(
                    ConfigurationFinding(
                        security_analysis_id=sec_record.id,
                        repository_id=repo.id,
                        file_path=c_res.file_path,
                        rule_name=c_res.rule_name,
                        severity=c_res.severity,
                        line_number=c_res.line_number,
                        description=c_res.description,
                    )
                )

            # Store Authentication
            for a_res in report.auth_findings:
                session.add(
                    AuthenticationFinding(
                        security_analysis_id=sec_record.id,
                        repository_id=repo.id,
                        auth_type=a_res.auth_type,
                        severity=a_res.severity,
                        file_path=a_res.file_path,
                        line_number=a_res.line_number,
                        description=a_res.description,
                    )
                )

            # Store Authorization
            for az_res in report.authz_findings:
                session.add(
                    AuthorizationFinding(
                        security_analysis_id=sec_record.id,
                        repository_id=repo.id,
                        authz_type=az_res.authz_type,
                        severity=az_res.severity,
                        file_path=az_res.file_path,
                        line_number=az_res.line_number,
                        description=az_res.description,
                    )
                )

            await session.commit()
            logger.info(f"Secrets detected: {report.secret_count}")
            logger.info(
                f"Dependency scan completed: {report.dependency_vuln_count} vulnerabilities"
            )
            logger.info(
                f"Configuration scan completed: {report.config_issues_count} issues"
            )
            logger.info(f"Rules executed: {len(report.findings)} findings")
            logger.info("Persistence complete")
            logger.info(f"Analysis finished for repository {repo.full_name}")

        except Exception as exc:
            logger.exception(
                f"Security analysis failed for repository {repo.full_name}: {exc}"
            )


@celery_app.task(name="app.tasks.security_tasks.security_analysis_task")
def security_analysis_task(
    repository_id: str, analysis_run_id: str | None = None
) -> None:
    """Celery task for running Security Intelligence Analysis."""
    asyncio.run(_async_run_security_analysis(repository_id, analysis_run_id))
