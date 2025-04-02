"""Create phone number column for Users

Revision ID: 7d7099640527
Revises:
Create Date: 2025-04-02 13:20:06.935127

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7d7099640527"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users", sa.Column("phone_number", sa.String(length=20), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone_number")
