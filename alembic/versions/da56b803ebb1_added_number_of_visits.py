"""Added number of visits

Revision ID: da56b803ebb1
Revises: 77fdcc3f1ca7
Create Date: 2023-12-03 18:55:10.371510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "da56b803ebb1"
down_revision: Union[str, None] = "77fdcc3f1ca7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("num_visits", sa.Integer(), server_default="0", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "num_visits")
    # ### end Alembic commands ###
