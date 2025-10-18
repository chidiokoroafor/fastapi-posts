"""add content column to posts

Revision ID: 6b38660016bd
Revises: 4ab22f4164ec
Create Date: 2025-10-17 18:41:20.532249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b38660016bd'
down_revision: Union[str, Sequence[str], None] = '4ab22f4164ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
