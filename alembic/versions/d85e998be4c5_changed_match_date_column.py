"""Changed match date column

Revision ID: d85e998be4c5
Revises: 632b14c57dc5
Create Date: 2023-11-07 16:12:27.479644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd85e998be4c5'
down_revision: Union[str, None] = '632b14c57dc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
