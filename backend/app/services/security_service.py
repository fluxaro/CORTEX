"""Security Intelligence service layer."""

import math
import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analyzers.security.engine import SecurityIntelligenceEngine
from app.exceptions.custom_exceptions import RepositoryNotFoundError
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


class SecurityService:
    """Service handling Security Intelligence (SAST) analysis and querying."""

    @staticmethod
    async def trigger_security_analysis(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> SecurityAnalysis:
        """Trigger synchronous Security Intelligence analysis for repository."""
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

        engine = SecurityIntelligenceEngine(target_path=repo.local_path)
        report = engine.run()

        sec_record = SecurityAnalysis(
            repository_id=repository_id,
            analysis_run_id=run_id,
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
        db.add(sec_record)
        await db.flush()

        for f_res in report.findings:
            db.add(
                SecurityFinding(
                    security_analysis_id=sec_record.id,
                    repository_id=repository_id,
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

        for s_res in report.secrets:
            db.add(
                SecretFinding(
                    security_analysis_id=sec_record.id,
                    repository_id=repository_id,
                    secret_type=s_res.secret_type,
                    severity=s_res.severity,
                    line_number=s_res.line_number,
                    file_path=s_res.file_path,
                    entropy=s_res.entropy,
                    masked_value=s_res.masked_value,
                    description=s_res.description,
                )
            )

        for d_res in report.dependencies:
            db.add(
                DependencyFinding(
                    security_analysis_id=sec_record.id,
                    repository_id=repository_id,
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

        for c_res in report.configs:
            db.add(
                ConfigurationFinding(
                    security_analysis_id=sec_record.id,
                    repository_id=repository_id,
                    file_path=c_res.file_path,
                    rule_name=c_res.rule_name,
                    severity=c_res.severity,
                    line_number=c_res.line_number,
                    description=c_res.description,
                )
            )

        for a_res in report.auth_findings:
            db.add(
                AuthenticationFinding(
                    security_analysis_id=sec_record.id,
                    repository_id=repository_id,
                    auth_type=a_res.auth_type,
                    severity=a_res.severity,
                    file_path=a_res.file_path,
                    line_number=a_res.line_number,
                    description=a_res.description,
                )
            )

        for az_res in report.authz_findings:
            db.add(
                AuthorizationFinding(
                    security_analysis_id=sec_record.id,
                    repository_id=repository_id,
                    authz_type=az_res.authz_type,
                    severity=az_res.severity,
                    file_path=az_res.file_path,
                    line_number=az_res.line_number,
                    description=az_res.description,
                )
            )

        await db.commit()
        return await SecurityService.get_latest_security(db, repository_id)

    @staticmethod
    async def get_latest_security(
        db: AsyncSession,
        repository_id: uuid.UUID,
    ) -> SecurityAnalysis:
        """Get latest security analysis report for repository."""
        query = (
            select(SecurityAnalysis)
            .options(
                selectinload(SecurityAnalysis.findings),
                selectinload(SecurityAnalysis.secrets),
                selectinload(SecurityAnalysis.dependencies),
                selectinload(SecurityAnalysis.configurations),
                selectinload(SecurityAnalysis.authentication_findings),
                selectinload(SecurityAnalysis.authorization_findings),
            )
            .where(SecurityAnalysis.repository_id == repository_id)
            .order_by(SecurityAnalysis.created_at.desc())
            .limit(1)
        )
        result = await db.execute(query)
        sec = result.scalar_one_or_none()
        if not sec:
            raise RepositoryNotFoundError(
                identifier=f"Security analysis for repository {repository_id}"
            )
        return sec

    @staticmethod
    async def list_findings(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        severity: str | None = None,
        language: str | None = None,
        category: str | None = None,
    ) -> dict[str, Any]:
        """List paginated SAST security findings."""
        latest_sec = await SecurityService.get_latest_security(db, repository_id)
        query = select(SecurityFinding).where(
            SecurityFinding.security_analysis_id == latest_sec.id
        )

        if severity:
            query = query.where(
                func.lower(SecurityFinding.severity) == severity.lower()
            )
        if language:
            query = query.where(
                func.lower(SecurityFinding.language) == language.lower()
            )
        if category:
            query = query.where(
                func.lower(SecurityFinding.category) == category.lower()
            )

        total = (
            await db.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()

        offset = (page - 1) * page_size
        items = list(
            (await db.execute(query.offset(offset).limit(page_size))).scalars().all()
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_secrets(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        secret_type: str | None = None,
        severity: str | None = None,
    ) -> dict[str, Any]:
        """List paginated secret findings."""
        latest_sec = await SecurityService.get_latest_security(db, repository_id)
        query = select(SecretFinding).where(
            SecretFinding.security_analysis_id == latest_sec.id
        )

        if secret_type:
            query = query.where(
                func.lower(SecretFinding.secret_type) == secret_type.lower()
            )
        if severity:
            query = query.where(func.lower(SecretFinding.severity) == severity.lower())

        total = (
            await db.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()

        offset = (page - 1) * page_size
        items = list(
            (await db.execute(query.offset(offset).limit(page_size))).scalars().all()
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_dependencies(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        severity: str | None = None,
    ) -> dict[str, Any]:
        """List paginated dependency vulnerability findings."""
        latest_sec = await SecurityService.get_latest_security(db, repository_id)
        query = select(DependencyFinding).where(
            DependencyFinding.security_analysis_id == latest_sec.id
        )

        if severity:
            query = query.where(
                func.lower(DependencyFinding.severity) == severity.lower()
            )

        total = (
            await db.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()

        offset = (page - 1) * page_size
        items = list(
            (await db.execute(query.offset(offset).limit(page_size))).scalars().all()
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_configurations(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        severity: str | None = None,
    ) -> dict[str, Any]:
        """List paginated configuration findings."""
        latest_sec = await SecurityService.get_latest_security(db, repository_id)
        query = select(ConfigurationFinding).where(
            ConfigurationFinding.security_analysis_id == latest_sec.id
        )

        if severity:
            query = query.where(
                func.lower(ConfigurationFinding.severity) == severity.lower()
            )

        total = (
            await db.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()

        offset = (page - 1) * page_size
        items = list(
            (await db.execute(query.offset(offset).limit(page_size))).scalars().all()
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_authentication(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        severity: str | None = None,
    ) -> dict[str, Any]:
        """List paginated authentication findings."""
        latest_sec = await SecurityService.get_latest_security(db, repository_id)
        query = select(AuthenticationFinding).where(
            AuthenticationFinding.security_analysis_id == latest_sec.id
        )

        if severity:
            query = query.where(
                func.lower(AuthenticationFinding.severity) == severity.lower()
            )

        total = (
            await db.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()

        offset = (page - 1) * page_size
        items = list(
            (await db.execute(query.offset(offset).limit(page_size))).scalars().all()
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }

    @staticmethod
    async def list_authorization(
        db: AsyncSession,
        repository_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        severity: str | None = None,
    ) -> dict[str, Any]:
        """List paginated authorization findings."""
        latest_sec = await SecurityService.get_latest_security(db, repository_id)
        query = select(AuthorizationFinding).where(
            AuthorizationFinding.security_analysis_id == latest_sec.id
        )

        if severity:
            query = query.where(
                func.lower(AuthorizationFinding.severity) == severity.lower()
            )

        total = (
            await db.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()

        offset = (page - 1) * page_size
        items = list(
            (await db.execute(query.offset(offset).limit(page_size))).scalars().all()
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(math.ceil(total / page_size), 1),
        }
