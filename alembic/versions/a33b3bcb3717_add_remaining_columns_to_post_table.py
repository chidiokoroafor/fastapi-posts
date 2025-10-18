"""Add remaining columns to post table

Revision ID: a33b3bcb3717
Revises: 786fc8b56b03
Create Date: 2025-10-18 13:53:32.073804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a33b3bcb3717'
down_revision: Union[str, Sequence[str], None] = '786fc8b56b03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False,server_default='TRUE'),)
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column('posts','created_at')
    pass
