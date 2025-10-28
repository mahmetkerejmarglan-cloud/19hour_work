"""add user table

Revision ID: 445fc660c96d
Revises: 725817673e3a
Create Date: 2025-10-28 12:28:12.347039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '445fc660c96d'
down_revision: Union[str, Sequence[str], None] = '725817673e3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
