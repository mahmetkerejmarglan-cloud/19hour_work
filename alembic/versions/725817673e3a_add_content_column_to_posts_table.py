"""add content column to posts table

Revision ID: 725817673e3a
Revises: 5109de6bed75
Create Date: 2025-10-28 12:03:37.403980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '725817673e3a'
down_revision: Union[str, Sequence[str], None] = '5109de6bed75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
