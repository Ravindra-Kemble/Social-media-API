"""add few columns to posts table

Revision ID: e7d5a538b645
Revises: 11b349827694
Create Date: 2024-01-22 00:29:03.249319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7d5a538b645'
down_revision: Union[str, None] = '11b349827694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
