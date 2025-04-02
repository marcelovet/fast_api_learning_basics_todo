"""Create Role table

Revision ID: 02bc9f1f2933
Revises: 7d7099640527
Create Date: 2025-04-02 13:33:16.512225

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "02bc9f1f2933"
down_revision: Union[str, None] = "7d7099640527"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("role_name", sa.String(length=256), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_name"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("roles")
