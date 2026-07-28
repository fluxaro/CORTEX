"""create repository iq tables

Revision ID: 006_create_repository_iq_tables
Revises: 005_create_maintainability_tables
Create Date: 2026-07-28

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "006_create_repository_iq_tables"
down_revision: Union[str, None] = "005_create_maintainability_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "repository_iqs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("maturity_level", sa.String(length=100), nullable=False),
        sa.Column("subsystem_scores", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_repository_iqs_id"), "repository_iqs", ["id"], unique=False)
    op.create_index(op.f("ix_repository_iqs_repository_id"), "repository_iqs", ["repository_id"], unique=False)

    op.create_table(
        "repository_summaries",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("executive_summary", sa.Text(), nullable=False),
        sa.Column("technical_summary", sa.Text(), nullable=False),
        sa.Column("architecture_summary", sa.Text(), nullable=False),
        sa.Column("security_summary", sa.Text(), nullable=False),
        sa.Column("maintainability_summary", sa.Text(), nullable=False),
        sa.Column("recruiter_summary", sa.Text(), nullable=False),
        sa.Column("engineering_manager_summary", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_iq_id"),
    )
    op.create_index(op.f("ix_repository_summaries_id"), "repository_summaries", ["id"], unique=False)

    op.create_table(
        "engineering_insights",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("weaknesses", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_iq_id"),
    )
    op.create_index(op.f("ix_engineering_insights_id"), "engineering_insights", ["id"], unique=False)

    op.create_table(
        "technical_debts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("total_hours", sa.Float(), nullable=False),
        sa.Column("total_days", sa.Float(), nullable=False),
        sa.Column("category_breakdown", sa.JSON(), nullable=False),
        sa.Column("items", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_iq_id"),
    )
    op.create_index(op.f("ix_technical_debts_id"), "technical_debts", ["id"], unique=False)

    op.create_table(
        "improvement_recommendations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("timeframe", sa.String(length=50), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("difficulty", sa.String(length=50), nullable=False),
        sa.Column("estimated_hours", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_improvement_recommendations_id"), "improvement_recommendations", ["id"], unique=False)

    op.create_table(
        "executive_summaries",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("report_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_iq_id"),
    )
    op.create_index(op.f("ix_executive_summaries_id"), "executive_summaries", ["id"], unique=False)

    op.create_table(
        "technical_summaries",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("report_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_iq_id"),
    )
    op.create_index(op.f("ix_technical_summaries_id"), "technical_summaries", ["id"], unique=False)

    op.create_table(
        "benchmark_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("overall_percentile", sa.Float(), nullable=False),
        sa.Column("quality_percentile", sa.Float(), nullable=False),
        sa.Column("security_percentile", sa.Float(), nullable=False),
        sa.Column("architecture_percentile", sa.Float(), nullable=False),
        sa.Column("maintainability_percentile", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_iq_id"),
    )
    op.create_index(op.f("ix_benchmark_results_id"), "benchmark_results", ["id"], unique=False)

    op.create_table(
        "ai_generations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_iq_id", sa.Uuid(), nullable=False),
        sa.Column("provider_name", sa.String(length=50), nullable=False),
        sa.Column("prompt_name", sa.String(length=100), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=False),
        sa.Column("response_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["repository_iq_id"], ["repository_iqs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_generations_id"), "ai_generations", ["id"], unique=False)

    op.create_table(
        "prompt_templates",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("template_name", sa.String(length=100), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("template_text", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("template_name"),
    )
    op.create_index(op.f("ix_prompt_templates_id"), "prompt_templates", ["id"], unique=False)
    op.create_index(op.f("ix_prompt_templates_template_name"), "prompt_templates", ["template_name"], unique=True)


def downgrade() -> None:
    op.drop_table("prompt_templates")
    op.drop_table("ai_generations")
    op.drop_table("benchmark_results")
    op.drop_table("technical_summaries")
    op.drop_table("executive_summaries")
    op.drop_table("improvement_recommendations")
    op.drop_table("technical_debts")
    op.drop_table("engineering_insights")
    op.drop_table("repository_summaries")
    op.drop_table("repository_iqs")
