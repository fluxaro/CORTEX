"""rebrand_iq_to_grade_report

Revision ID: 008_rebrand_iq_to_grade_report
Revises: 007_create_enterprise_tables
Create Date: 2026-08-18 19:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "008_rebrand_iq_to_grade_report"
down_revision: Union[str, None] = "007_create_enterprise_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename repository_iqs to repository_grade_reports
    op.rename_table("repository_iqs", "repository_grade_reports")

    # Add new grade columns to repository_grade_reports
    op.add_column(
        "repository_grade_reports",
        sa.Column("overall_grade", sa.String(length=10), nullable=False, server_default="C"),
    )
    op.add_column(
        "repository_grade_reports",
        sa.Column("capped", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "repository_grade_reports",
        sa.Column("cap_reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "repository_grade_reports",
        sa.Column("category_scores", sa.JSON(), nullable=False, server_default="{}"),
    )


def downgrade() -> None:
    op.drop_column("repository_grade_reports", "category_scores")
    op.drop_column("repository_grade_reports", "cap_reason")
    op.drop_column("repository_grade_reports", "capped")
    op.drop_column("repository_grade_reports", "overall_grade")
    op.rename_table("repository_grade_reports", "repository_iqs")
