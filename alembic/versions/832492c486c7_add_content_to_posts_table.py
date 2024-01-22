"""add content to posts table

Revision ID: 832492c486c7
Revises: 09a5d75321c8
Create Date: 2024-01-21 23:36:33.420877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '832492c486c7'
down_revision: Union[str, None] = '09a5d75321c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
