"""Changed managers fotmob id

Revision ID: 3cfc3dc6519e
Revises: f4b33de1f7ae
Create Date: 2023-11-09 10:31:41.425460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cfc3dc6519e'
down_revision: Union[str, None] = 'f4b33de1f7ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('managers_fotmob_id_key', 'managers', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('managers_fotmob_id_key', 'managers', ['fotmob_id'])
    # ### end Alembic commands ###
