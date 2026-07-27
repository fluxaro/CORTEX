"""create analysis tables

Revision ID: 002_create_analysis_tables
Revises: 001_create_repository_tables
Create Date: 2026-07-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "002_create_analysis_tables"
down_revision: Union[str, None] = "001_create_repository_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("commit_hash", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_analysis_runs_id"), "analysis_runs", ["id"], unique=False)
    op.create_index(op.f("ix_analysis_runs_repository_id"), "analysis_runs", ["repository_id"], unique=False)
    op.create_index(op.f("ix_analysis_runs_status"), "analysis_runs", ["status"], unique=False)

    op.create_table(
        "repository_metrics",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("total_files", sa.Integer(), nullable=False),
        sa.Column("source_files", sa.Integer(), nullable=False),
        sa.Column("test_files", sa.Integer(), nullable=False),
        sa.Column("blank_lines", sa.Integer(), nullable=False),
        sa.Column("comment_lines", sa.Integer(), nullable=False),
        sa.Column("code_lines", sa.Integer(), nullable=False),
        sa.Column("total_loc", sa.Integer(), nullable=False),
        sa.Column("comment_ratio", sa.Float(), nullable=False),
        sa.Column("avg_complexity", sa.Float(), nullable=False),
        sa.Column("max_complexity", sa.Integer(), nullable=False),
        sa.Column("complexity_rank", sa.String(length=5), nullable=False),
        sa.Column("maintainability_index", sa.Float(), nullable=False),
        sa.Column("duplicate_percentage", sa.Float(), nullable=False),
        sa.Column("file_extension_dist", sa.JSON(), nullable=False),
        sa.Column("language_dist", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_repository_metrics_id"), "repository_metrics", ["id"], unique=False)
    op.create_index(op.f("ix_repository_metrics_repository_id"), "repository_metrics", ["repository_id"], unique=False)

    op.create_table(
        "file_metrics",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("path", sa.String(length=1024), nullable=False),
        sa.Column("language", sa.String(length=100), nullable=False),
        sa.Column("loc", sa.Integer(), nullable=False),
        sa.Column("comment_lines", sa.Integer(), nullable=False),
        sa.Column("blank_lines", sa.Integer(), nullable=False),
        sa.Column("code_lines", sa.Integer(), nullable=False),
        sa.Column("function_count", sa.Integer(), nullable=False),
        sa.Column("class_count", sa.Integer(), nullable=False),
        sa.Column("import_count", sa.Integer(), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("complexity", sa.Integer(), nullable=False),
        sa.Column("maintainability_index", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_file_metrics_id"), "file_metrics", ["id"], unique=False)
    op.create_index(op.f("ix_file_metrics_analysis_run_id"), "file_metrics", ["analysis_run_id"], unique=False)
    op.create_index(op.f("ix_file_metrics_path"), "file_metrics", ["path"], unique=False)

    op.create_table(
        "function_metrics",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("file_metrics_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("class_name", sa.String(length=255), nullable=True),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("return_annotation", sa.String(length=255), nullable=True),
        sa.Column("decorators", sa.JSON(), nullable=False),
        sa.Column("visibility", sa.String(length=50), nullable=False),
        sa.Column("method_type", sa.String(length=50), nullable=False),
        sa.Column("line_count", sa.Integer(), nullable=False),
        sa.Column("complexity", sa.Integer(), nullable=False),
        sa.Column("nesting_depth", sa.Integer(), nullable=False),
        sa.Column("maintainability", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["file_metrics_id"], ["file_metrics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_function_metrics_id"), "function_metrics", ["id"], unique=False)
    op.create_index(op.f("ix_function_metrics_name"), "function_metrics", ["name"], unique=False)

    op.create_table(
        "class_metrics",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("file_metrics_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_classes", sa.JSON(), nullable=False),
        sa.Column("methods_count", sa.Integer(), nullable=False),
        sa.Column("fields_count", sa.Integer(), nullable=False),
        sa.Column("property_count", sa.Integer(), nullable=False),
        sa.Column("public_methods", sa.Integer(), nullable=False),
        sa.Column("private_methods", sa.Integer(), nullable=False),
        sa.Column("static_methods", sa.Integer(), nullable=False),
        sa.Column("abstract_methods", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["file_metrics_id"], ["file_metrics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_class_metrics_id"), "class_metrics", ["id"], unique=False)
    op.create_index(op.f("ix_class_metrics_name"), "class_metrics", ["name"], unique=False)

    op.create_table(
        "duplicate_groups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("duplicate_hash", sa.String(length=128), nullable=False),
        sa.Column("line_count", sa.Integer(), nullable=False),
        sa.Column("instance_count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_duplicate_groups_id"), "duplicate_groups", ["id"], unique=False)

    op.create_table(
        "duplicate_files",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("duplicate_group_id", sa.Uuid(), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("start_line", sa.Integer(), nullable=False),
        sa.Column("end_line", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["duplicate_group_id"], ["duplicate_groups.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_duplicate_files_id"), "duplicate_files", ["id"], unique=False)

    op.create_table(
        "code_smells",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("smell_type", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("symbol_name", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_code_smells_id"), "code_smells", ["id"], unique=False)
    op.create_index(op.f("ix_code_smells_file_path"), "code_smells", ["file_path"], unique=False)
    op.create_index(op.f("ix_code_smells_smell_type"), "code_smells", ["smell_type"], unique=False)


def downgrade() -> None:
    op.drop_table("code_smells")
    op.drop_table("duplicate_files")
    op.drop_table("duplicate_groups")
    op.drop_table("class_metrics")
    op.drop_table("function_metrics")
    op.drop_table("file_metrics")
    op.drop_table("repository_metrics")
    op.drop_table("analysis_runs")
