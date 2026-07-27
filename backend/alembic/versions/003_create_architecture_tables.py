"""create architecture tables

Revision ID: 003_create_architecture_tables
Revises: 002_create_analysis_tables
Create Date: 2026-07-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "003_create_architecture_tables"
down_revision: Union[str, None] = "002_create_analysis_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "architecture_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=False),
        sa.Column("arch_style", sa.String(length=100), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("layer_separation_score", sa.Float(), nullable=False),
        sa.Column("dependency_direction_score", sa.Float(), nullable=False),
        sa.Column("pattern_confidence", sa.Float(), nullable=False),
        sa.Column("project_organization_score", sa.Float(), nullable=False),
        sa.Column("coupling_score", sa.Float(), nullable=False),
        sa.Column("modularity_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_run_id"),
    )
    op.create_index(op.f("ix_architecture_analyses_id"), "architecture_analyses", ["id"], unique=False)
    op.create_index(op.f("ix_architecture_analyses_repository_id"), "architecture_analyses", ["repository_id"], unique=False)

    op.create_table(
        "architecture_layers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("architecture_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("file_paths", sa.JSON(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["architecture_analysis_id"], ["architecture_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_architecture_layers_id"), "architecture_layers", ["id"], unique=False)

    op.create_table(
        "architecture_violations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("architecture_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("violation_type", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("source_path", sa.String(length=1024), nullable=False),
        sa.Column("target_path", sa.String(length=1024), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["architecture_analysis_id"], ["architecture_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_architecture_violations_id"), "architecture_violations", ["id"], unique=False)

    op.create_table(
        "detected_patterns",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("architecture_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("pattern_name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("location", sa.String(length=1024), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["architecture_analysis_id"], ["architecture_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_detected_patterns_id"), "detected_patterns", ["id"], unique=False)

    op.create_table(
        "dependency_graphs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("architecture_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("total_nodes", sa.Integer(), nullable=False),
        sa.Column("total_edges", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["architecture_analysis_id"], ["architecture_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("architecture_analysis_id"),
    )
    op.create_index(op.f("ix_dependency_graphs_id"), "dependency_graphs", ["id"], unique=False)

    op.create_table(
        "dependency_nodes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("dependency_graph_id", sa.Uuid(), nullable=False),
        sa.Column("node_identifier", sa.String(length=512), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("node_type", sa.String(length=50), nullable=False),
        sa.Column("layer_name", sa.String(length=100), nullable=True),
        sa.Column("path", sa.String(length=1024), nullable=True),
        sa.ForeignKeyConstraint(["dependency_graph_id"], ["dependency_graphs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dependency_nodes_id"), "dependency_nodes", ["id"], unique=False)

    op.create_table(
        "dependency_edges",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("dependency_graph_id", sa.Uuid(), nullable=False),
        sa.Column("source_node_id", sa.String(length=512), nullable=False),
        sa.Column("target_node_id", sa.String(length=512), nullable=False),
        sa.Column("import_type", sa.String(length=50), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["dependency_graph_id"], ["dependency_graphs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dependency_edges_id"), "dependency_edges", ["id"], unique=False)

    op.create_table(
        "framework_detections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("architecture_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("detected_version", sa.String(length=50), nullable=True),
        sa.Column("is_convention_compliant", sa.Boolean(), nullable=False),
        sa.Column("convention_findings", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["architecture_analysis_id"], ["architecture_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_framework_detections_id"), "framework_detections", ["id"], unique=False)

    op.create_table(
        "technology_stacks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("architecture_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("languages", sa.JSON(), nullable=False),
        sa.Column("frameworks", sa.JSON(), nullable=False),
        sa.Column("orms", sa.JSON(), nullable=False),
        sa.Column("databases", sa.JSON(), nullable=False),
        sa.Column("cloud", sa.JSON(), nullable=False),
        sa.Column("ci_cd", sa.JSON(), nullable=False),
        sa.Column("package_managers", sa.JSON(), nullable=False),
        sa.Column("build_tools", sa.JSON(), nullable=False),
        sa.Column("testing_frameworks", sa.JSON(), nullable=False),
        sa.Column("formatters", sa.JSON(), nullable=False),
        sa.Column("linters", sa.JSON(), nullable=False),
        sa.Column("containers", sa.JSON(), nullable=False),
        sa.Column("caching", sa.JSON(), nullable=False),
        sa.Column("auth", sa.JSON(), nullable=False),
        sa.Column("api_surfaces", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["architecture_analysis_id"], ["architecture_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("architecture_analysis_id"),
    )
    op.create_index(op.f("ix_technology_stacks_id"), "technology_stacks", ["id"], unique=False)

    op.create_table(
        "architecture_recommendation_placeholders",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("architecture_analysis_id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["architecture_analysis_id"], ["architecture_analyses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_architecture_recommendation_placeholders_id"), "architecture_recommendation_placeholders", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("architecture_recommendation_placeholders")
    op.drop_table("technology_stacks")
    op.drop_table("framework_detections")
    op.drop_table("dependency_edges")
    op.drop_table("dependency_nodes")
    op.drop_table("dependency_graphs")
    op.drop_table("detected_patterns")
    op.drop_table("architecture_violations")
    op.drop_table("architecture_layers")
    op.drop_table("architecture_analyses")
