"""Database models for Security Intelligence findings and metrics."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now


class SecurityAnalysis(Base):
    """Aggregated security intelligence run metrics for a repository."""

    __tablename__ = "security_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    critical_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    high_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    medium_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    low_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    info_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    secret_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    dependency_vuln_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    config_issues_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    auth_issues_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    # Relationships
    findings: Mapped[list["SecurityFinding"]] = relationship(
        "SecurityFinding",
        back_populates="security_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    secrets: Mapped[list["SecretFinding"]] = relationship(
        "SecretFinding",
        back_populates="security_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    dependencies: Mapped[list["DependencyFinding"]] = relationship(
        "DependencyFinding",
        back_populates="security_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    configurations: Mapped[list["ConfigurationFinding"]] = relationship(
        "ConfigurationFinding",
        back_populates="security_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    authentication_findings: Mapped[list["AuthenticationFinding"]] = relationship(
        "AuthenticationFinding",
        back_populates="security_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    authorization_findings: Mapped[list["AuthorizationFinding"]] = relationship(
        "AuthorizationFinding",
        back_populates="security_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class SecurityFinding(Base):
    """SAST rule security finding."""

    __tablename__ = "security_findings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    rule_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    rule_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(
        String(50), default="HIGH", nullable=False, index=True
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.85, nullable=False)

    language: Mapped[str] = mapped_column(
        String(50), default="Python", nullable=False, index=True
    )
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    line_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    column_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)
    remediation_placeholder: Mapped[str] = mapped_column(
        Text, default="Sanitize input", nullable=False
    )
    reference_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    cvss_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    security_analysis: Mapped[SecurityAnalysis] = relationship(
        "SecurityAnalysis", back_populates="findings"
    )


class SecretFinding(Base):
    """Committed secret or API key finding."""

    __tablename__ = "secret_findings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    secret_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(
        String(50), default="CRITICAL", nullable=False, index=True
    )
    line_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    entropy: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    masked_value: Mapped[str] = mapped_column(
        String(100), default="********", nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    security_analysis: Mapped[SecurityAnalysis] = relationship(
        "SecurityAnalysis", back_populates="secrets"
    )


class DependencyFinding(Base):
    """Vulnerable or unmaintained dependency finding."""

    __tablename__ = "dependency_findings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    package_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    cve_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    cvss_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    severity: Mapped[str] = mapped_column(
        String(50), default="HIGH", nullable=False, index=True
    )
    license: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    references: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    security_analysis: Mapped[SecurityAnalysis] = relationship(
        "SecurityAnalysis", back_populates="dependencies"
    )


class ConfigurationFinding(Base):
    """Infrastructure misconfiguration finding."""

    __tablename__ = "configuration_findings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    rule_name: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(
        String(50), default="HIGH", nullable=False, index=True
    )
    line_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    security_analysis: Mapped[SecurityAnalysis] = relationship(
        "SecurityAnalysis", back_populates="configurations"
    )


class AuthenticationFinding(Base):
    """Authentication mechanism weakness finding."""

    __tablename__ = "authentication_findings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    auth_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(
        String(50), default="HIGH", nullable=False, index=True
    )
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    security_analysis: Mapped[SecurityAnalysis] = relationship(
        "SecurityAnalysis", back_populates="authentication_findings"
    )


class AuthorizationFinding(Base):
    """Authorization / RBAC weakness finding."""

    __tablename__ = "authorization_findings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    authz_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(
        String(50), default="HIGH", nullable=False, index=True
    )
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    security_analysis: Mapped[SecurityAnalysis] = relationship(
        "SecurityAnalysis", back_populates="authorization_findings"
    )


class SecurityRule(Base):
    """Security rule definition."""

    __tablename__ = "security_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    rule_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    rule_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class SecurityReference(Base):
    """External security reference link."""

    __tablename__ = "security_references"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_finding_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_findings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)


class SecuritySummary(Base):
    """Summary metrics and most vulnerable files."""

    __tablename__ = "security_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    security_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("security_analyses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    most_vulnerable_files: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )
    top_rule_violations: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )
