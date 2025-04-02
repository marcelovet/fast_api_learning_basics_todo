"""Add foreign key for role in users alter column

Revision ID: 154a373623cb
Revises: 02bc9f1f2933
Create Date: 2025-04-02 13:38:06.207514

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "154a373623cb"
down_revision: Union[str, None] = "02bc9f1f2933"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users", "role", existing_type=sa.VARCHAR(length=256), nullable=True
    )
    op.create_foreign_key(
        "fk_users_role_roles",
        "users",
        "roles",
        ["role"],
        ["role_name"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_users_role_roles", "users", type_="foreignkey")
