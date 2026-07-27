"""create repository tables

Revision ID: 001_create_repository_tables
Revises:
Create Date: 2026-07-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001_create_repository_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "repositories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("owner", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=512), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("default_branch", sa.String(length=255), nullable=False),
        sa.Column("stars", sa.Integer(), nullable=False),
        sa.Column("forks", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(length=100), nullable=True),
        sa.Column("license", sa.String(length=255), nullable=True),
        sa.Column("clone_url", sa.String(length=1024), nullable=False),
        sa.Column("html_url", sa.String(length=1024), nullable=False),
        sa.Column("visibility", sa.String(length=50), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_pushed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("analysis_status", sa.String(length=50), nullable=False),
        sa.Column("local_path", sa.String(length=1024), nullable=True),
        sa.Column("created_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_on", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("full_name"),
    )
    op.create_index(op.f("ix_repositories_id"), "repositories", ["id"], unique=False)
    op.create_index(op.f("ix_repositories_owner"), "repositories", ["owner"], unique=False)
    op.create_index(op.f("ix_repositories_language"), "repositories", ["language"], unique=False)
    op.create_index(op.f("ix_repositories_status"), "repositories", ["status"], unique=False)

    op.create_table(
        "repository_file_indices",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("repository_id", sa.Uuid(), nullable=False),
        sa.Column("folder_count", sa.Integer(), nullable=False),
        sa.Column("file_count", sa.Integer(), nullable=False),
        sa.Column("max_depth", sa.Integer(), nullable=False),
        sa.Column("total_size_bytes", sa.Integer(), nullable=False),
        sa.Column("largest_files", sa.JSON(), nullable=False),
        sa.Column("file_extensions", sa.JSON(), nullable=False),
        sa.Column("language_distribution", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_id"),
    )
    op.create_index(op.f("ix_repository_file_indices_id"), "repository_file_indices", ["id"], unique=False)
    op.create_index(op.f("ix_repository_file_indices_repository_id"), "repository_file_indices", ["repository_id"], unique=True)


def downgrade() -> None:
    op.drop_table("repository_file_indices")
    op.drop_table("repositories")
