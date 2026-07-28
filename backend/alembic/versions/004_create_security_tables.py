"""create security tables

Revision ID: 004_create_security_tables
Revises: 003_create_architecture_tables
Create Date: 2026-07-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "004_create_security_tables"
down_revision: Union[str, None] = "003_create_architecture_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "security_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("critical_count", sa.Integer(), nullable=False),
        sa.Column("high_count", sa.Integer(), nullable=False),
        sa.Column("medium_count", sa.Integer(), nullable=False),
        sa.Column("low_count", sa.Integer(), nullable=False),
        sa.Column("info_count", sa.Integer(), nullable=False),
        sa.Column("secret_count", sa.Integer(), nullable=False),
        sa.Column("dependency_vuln_count", sa.Integer(), nullable=False),
        sa.Column("config_issues_count", sa.Integer(), nullable=False),
        sa.Column("auth_issues_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_security_analyses_id"), "security_analyses", ["id"], unique=False)
    op.create_index(op.f("ix_security_analyses_repository_id"), "security_analyses", ["repository_id"], unique=False)

    op.create_table(
        "security_findings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("rule_id", sa.String(length=50), nullable=False),
        sa.Column("rule_name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("language", sa.String(length=50), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("column_number", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("remediation_placeholder", sa.Text(), nullable=False),
        sa.Column("reference_url", sa.String(length=1024), nullable=True),
        sa.Column("cvss_score", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["security_analysis_id"], ["security_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_security_findings_category"), "security_findings", ["category"], unique=False)
    op.create_index(op.f("ix_security_findings_file_path"), "security_findings", ["file_path"], unique=False)
    op.create_index(op.f("ix_security_findings_id"), "security_findings", ["id"], unique=False)
    op.create_index(op.f("ix_security_findings_language"), "security_findings", ["language"], unique=False)
    op.create_index(op.f("ix_security_findings_rule_id"), "security_findings", ["rule_id"], unique=False)
    op.create_index(op.f("ix_security_findings_severity"), "security_findings", ["severity"], unique=False)

    op.create_table(
        "secret_findings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("secret_type", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("entropy", sa.Float(), nullable=False),
        sa.Column("masked_value", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["security_analysis_id"], ["security_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_secret_findings_file_path"), "secret_findings", ["file_path"], unique=False)
    op.create_index(op.f("ix_secret_findings_id"), "secret_findings", ["id"], unique=False)
    op.create_index(op.f("ix_secret_findings_secret_type"), "secret_findings", ["secret_type"], unique=False)
    op.create_index(op.f("ix_secret_findings_severity"), "secret_findings", ["severity"], unique=False)

    op.create_table(
        "dependency_findings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("package_name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=100), nullable=False),
        sa.Column("cve_id", sa.String(length=100), nullable=True),
        sa.Column("cvss_score", sa.Float(), nullable=True),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("license", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("references", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["security_analysis_id"], ["security_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dependency_findings_cve_id"), "dependency_findings", ["cve_id"], unique=False)
    op.create_index(op.f("ix_dependency_findings_id"), "dependency_findings", ["id"], unique=False)
    op.create_index(op.f("ix_dependency_findings_package_name"), "dependency_findings", ["package_name"], unique=False)
    op.create_index(op.f("ix_dependency_findings_severity"), "dependency_findings", ["severity"], unique=False)

    op.create_table(
        "configuration_findings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("rule_name", sa.String(length=255), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["security_analysis_id"], ["security_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_configuration_findings_file_path"), "configuration_findings", ["file_path"], unique=False)
    op.create_index(op.f("ix_configuration_findings_id"), "configuration_findings", ["id"], unique=False)
    op.create_index(op.f("ix_configuration_findings_severity"), "configuration_findings", ["severity"], unique=False)

    op.create_table(
        "authentication_findings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("auth_type", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["security_analysis_id"], ["security_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_authentication_findings_auth_type"), "authentication_findings", ["auth_type"], unique=False)
    op.create_index(op.f("ix_authentication_findings_id"), "authentication_findings", ["id"], unique=False)
    op.create_index(op.f("ix_authentication_findings_severity"), "authentication_findings", ["severity"], unique=False)

    op.create_table(
        "authorization_findings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("authz_type", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["security_analysis_id"], ["security_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_authorization_findings_authz_type"), "authorization_findings", ["authz_type"], unique=False)
    op.create_index(op.f("ix_authorization_findings_id"), "authorization_findings", ["id"], unique=False)
    op.create_index(op.f("ix_authorization_findings_severity"), "authorization_findings", ["severity"], unique=False)

    op.create_table(
        "security_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("rule_id", sa.String(length=50), nullable=False),
        sa.Column("rule_name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rule_id"),
    )
    op.create_index(op.f("ix_security_rules_id"), "security_rules", ["id"], unique=False)
    op.create_index(op.f("ix_security_rules_rule_id"), "security_rules", ["rule_id"], unique=True)

    op.create_table(
        "security_references",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_finding_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=False),
        sa.ForeignKeyConstraint(["security_finding_id"], ["security_findings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_security_references_id"), "security_references", ["id"], unique=False)

    op.create_table(
        "security_summaries",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("security_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("most_vulnerable_files", sa.JSON(), nullable=False),
        sa.Column("top_rule_violations", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["security_analysis_id"], ["security_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("security_analysis_id"),
    )
    op.create_index(op.f("ix_security_summaries_id"), "security_summaries", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("security_summaries")
    op.drop_table("security_references")
    op.drop_table("security_rules")
    op.drop_table("authorization_findings")
    op.drop_table("authentication_findings")
    op.drop_table("configuration_findings")
    op.drop_table("dependency_findings")
    op.drop_table("secret_findings")
    op.drop_table("security_findings")
    op.drop_table("security_analyses")
