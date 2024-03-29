"""initial

Revision ID: 4f3219b61c8b
Revises: 
Create Date: 2024-01-08 01:31:28.862432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

import bot

# revision identifiers, used by Alembic.
revision: str = '4f3219b61c8b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('upd_date', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.VARCHAR(length=32), nullable=True),
        sa.Column('balance', sa.Integer(), nullable=True),
        sa.Column('locale', sa.VARCHAR(length=2), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('user_id')
    )

    op.create_table('channels',
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('upd_date', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('admin_id', sa.Integer(), nullable=True),
        sa.Column('subs_count', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['admin_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )

    op.create_table('posts',
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('upd_date', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('text', mysql.TEXT(), nullable=False),
        sa.Column('budget', sa.Integer(), nullable=True),
        sa.Column('pr_type', sa.Enum('NONE', 'CLICKS', 'PUBLICATIONS', name='prtype'), nullable=True),
        sa.Column('pub_price', sa.Integer(), nullable=False),
        sa.Column('url_price', sa.Integer(), nullable=False),
        sa.Column('subs_min', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('post_channels',
        sa.Column('post', sa.Integer(), nullable=False),
        sa.Column('channel', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['channel'], ['channels.id'], ),
        sa.ForeignKeyConstraint(['post'], ['posts.id'], ),
        sa.PrimaryKeyConstraint('post', 'channel')
    )

    op.create_table('urls',
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('upd_date', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('url', bot.db.types.url.URLType(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=True),
        sa.Column('clicks_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    op.drop_table('post_channels')
    op.drop_table('posts')
    op.drop_table('channels')
    op.drop_table('users')
    # ### end Alembic commands ###
