"""Initial Alembic

Revision ID: 77fdcc3f1ca7
Revises: 
Create Date: 2023-11-30 21:07:53.335597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77fdcc3f1ca7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lastrow',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('last_row', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'last_row')
    )
    op.create_table('nations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('flag', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('season',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('season', sa.String(length=9), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('current_team', sa.Boolean(), server_default='False', nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('api_key', sa.String(), nullable=True),
    sa.Column('admin', sa.Boolean(), server_default='False', nullable=True),
    sa.Column('is_verified', sa.Boolean(), server_default='False', nullable=True),
    sa.Column('verification_code', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_key'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('verification_code')
    )
    op.create_table('managers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nation_id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['nation_id'], ['nations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matches',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('home_id', sa.Integer(), nullable=True),
    sa.Column('home_score', sa.Integer(), server_default='0', nullable=True),
    sa.Column('away_id', sa.Integer(), nullable=True),
    sa.Column('away_score', sa.Integer(), server_default='0', nullable=True),
    sa.Column('match_date', sa.DATE(), server_default='now()', nullable=True),
    sa.Column('season', sa.String(length=9), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['away_id'], ['teams.id'], ),
    sa.ForeignKeyConstraint(['home_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stints',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('date_start', sa.DATE(), nullable=False),
    sa.Column('date_end', sa.DATE(), nullable=True),
    sa.Column('current', sa.Boolean(), server_default='False', nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stints')
    op.drop_table('matches')
    op.drop_table('managers')
    op.drop_table('users')
    op.drop_table('teams')
    op.drop_table('season')
    op.drop_table('nations')
    op.drop_table('lastrow')
    # ### end Alembic commands ###