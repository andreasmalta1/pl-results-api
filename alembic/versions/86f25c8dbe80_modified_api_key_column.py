"""Modified API key column

Revision ID: 86f25c8dbe80
Revises: 475714254e86
Create Date: 2023-11-16 14:48:32.942730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86f25c8dbe80'
down_revision: Union[str, None] = '475714254e86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'api_key',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'api_key',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###