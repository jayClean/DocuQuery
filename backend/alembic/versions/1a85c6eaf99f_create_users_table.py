"""Create users table

Revision ID: 1a85c6eaf99f
Revises: 
Create Date: 2024-10-22 01:41:17.739334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a85c6eaf99f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_users_email'), 'users', ['email'], unique=True, schema='public')
    op.create_index(op.f('ix_public_users_id'), 'users', ['id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_users_username'), 'users', ['username'], unique=True, schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_public_users_username'), table_name='users', schema='public')
    op.drop_index(op.f('ix_public_users_id'), table_name='users', schema='public')
    op.drop_index(op.f('ix_public_users_email'), table_name='users', schema='public')
    op.drop_table('users', schema='public')
    # ### end Alembic commands ###
