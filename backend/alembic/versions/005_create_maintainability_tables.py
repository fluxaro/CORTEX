"""create maintainability tables

Revision ID: 005_create_maintainability_tables
Revises: 004_create_security_tables
Create Date: 2026-07-28

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "005_create_maintainability_tables"
down_revision: Union[str, None] = "004_create_security_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documentation_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("documentation_score", sa.Float(), nullable=False),
        sa.Column("has_architecture_docs", sa.Boolean(), nullable=False),
        sa.Column("has_api_docs", sa.Boolean(), nullable=False),
        sa.Column("has_deployment_guide", sa.Boolean(), nullable=False),
        sa.Column("has_dev_guide", sa.Boolean(), nullable=False),
        sa.Column("doc_frameworks", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_documentation_analyses_id"), "documentation_analyses", ["id"], unique=False)
    op.create_index(op.f("ix_documentation_analyses_repository_id"), "documentation_analyses", ["repository_id"], unique=False)

    op.create_table(
        "documentation_sections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("documentation_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("section_name", sa.String(length=100), nullable=False),
        sa.Column("is_present", sa.Boolean(), nullable=False),
        sa.Column("content_snippet", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["documentation_analysis_id"], ["documentation_analyses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_documentation_sections_id"), "documentation_sections", ["id"], unique=False)

    op.create_table(
        "readme_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("documentation_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("completeness_percentage", sa.Float(), nullable=False),
        sa.Column("missing_sections", sa.JSON(), nullable=False),
        sa.Column("detected_sections", sa.JSON(), nullable=False),
        sa.Column("has_badges", sa.Boolean(), nullable=False),
        sa.Column("has_screenshots", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["documentation_analysis_id"], ["documentation_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("documentation_analysis_id"),
    )
    op.create_index(op.f("ix_readme_analyses_id"), "readme_analyses", ["id"], unique=False)

    op.create_table(
        "testing_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("testing_score", sa.Float(), nullable=False),
        sa.Column("frameworks", sa.JSON(), nullable=False),
        sa.Column("test_file_count", sa.Integer(), nullable=False),
        sa.Column("estimated_test_count", sa.Integer(), nullable=False),
        sa.Column("has_unit_tests", sa.Boolean(), nullable=False),
        sa.Column("has_integration_tests", sa.Boolean(), nullable=False),
        sa.Column("has_e2e_tests", sa.Boolean(), nullable=False),
        sa.Column("has_mocks", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_testing_analyses_id"), "testing_analyses", ["id"], unique=False)

    op.create_table(
        "git_history_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("commit_count", sa.Integer(), nullable=False),
        sa.Column("contributor_count", sa.Integer(), nullable=False),
        sa.Column("branch_count", sa.Integer(), nullable=False),
        sa.Column("tag_count", sa.Integer(), nullable=False),
        sa.Column("repo_age_days", sa.Integer(), nullable=False),
        sa.Column("commits_per_week", sa.Float(), nullable=False),
        sa.Column("inactive_periods_count", sa.Integer(), nullable=False),
        sa.Column("development_velocity_score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_git_history_analyses_id"), "git_history_analyses", ["id"], unique=False)

    op.create_table(
        "commit_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("git_history_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("commit_quality_score", sa.Float(), nullable=False),
        sa.Column("conventional_commits_percentage", sa.Float(), nullable=False),
        sa.Column("generic_commits_percentage", sa.Float(), nullable=False),
        sa.Column("commit_types_breakdown", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["git_history_analysis_id"], ["git_history_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("git_history_analysis_id"),
    )
    op.create_index(op.f("ix_commit_analyses_id"), "commit_analyses", ["id"], unique=False)

    op.create_table(
        "release_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("release_score", sa.Float(), nullable=False),
        sa.Column("release_count", sa.Integer(), nullable=False),
        sa.Column("has_changelog", sa.Boolean(), nullable=False),
        sa.Column("uses_semver", sa.Boolean(), nullable=False),
        sa.Column("latest_release_tag", sa.String(length=100), nullable=True),
        sa.Column("days_since_last_release", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_release_analyses_id"), "release_analyses", ["id"], unique=False)

    op.create_table(
        "community_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("community_score", sa.Float(), nullable=False),
        sa.Column("has_contributing", sa.Boolean(), nullable=False),
        sa.Column("has_code_of_conduct", sa.Boolean(), nullable=False),
        sa.Column("has_security_policy", sa.Boolean(), nullable=False),
        sa.Column("has_issue_templates", sa.Boolean(), nullable=False),
        sa.Column("has_pr_templates", sa.Boolean(), nullable=False),
        sa.Column("has_discussions", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_community_analyses_id"), "community_analyses", ["id"], unique=False)

    op.create_table(
        "ci_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("ci_score", sa.Float(), nullable=False),
        sa.Column("providers", sa.JSON(), nullable=False),
        sa.Column("has_test_jobs", sa.Boolean(), nullable=False),
        sa.Column("has_lint_jobs", sa.Boolean(), nullable=False),
        sa.Column("has_security_scans", sa.Boolean(), nullable=False),
        sa.Column("has_build_jobs", sa.Boolean(), nullable=False),
        sa.Column("has_deploy_jobs", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_ci_analyses_id"), "ci_analyses", ["id"], unique=False)

    op.create_table(
        "license_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("spdx_identifier", sa.String(length=50), nullable=False),
        sa.Column("is_osi_approved", sa.Boolean(), nullable=False),
        sa.Column("has_license_file", sa.Boolean(), nullable=False),
        sa.Column("is_consistent", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_license_analyses_id"), "license_analyses", ["id"], unique=False)

    op.create_table(
        "maintainability_metrics",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("documentation_score", sa.Float(), nullable=False),
        sa.Column("testing_score", sa.Float(), nullable=False),
        sa.Column("ci_score", sa.Float(), nullable=False),
        sa.Column("release_score", sa.Float(), nullable=False),
        sa.Column("repository_health_score", sa.Float(), nullable=False),
        sa.Column("community_score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_maintainability_metrics_id"), "maintainability_metrics", ["id"], unique=False)

    op.create_table(
        "repository_healths",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("repository_health_score", sa.Float(), nullable=False),
        sa.Column("maintenance_frequency_score", sa.Float(), nullable=False),
        sa.Column("community_readiness_score", sa.Float(), nullable=False),
        sa.Column("contribution_readiness_score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_repository_healths_id"), "repository_healths", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("repository_healths")
    op.drop_table("maintainability_metrics")
    op.drop_table("license_analyses")
    op.drop_table("ci_analyses")
    op.drop_table("community_analyses")
    op.drop_table("release_analyses")
    op.drop_table("commit_analyses")
    op.drop_table("git_history_analyses")
    op.drop_table("testing_analyses")
    op.drop_table("readme_analyses")
    op.drop_table("documentation_sections")
    op.drop_table("documentation_analyses")
