"""initial

Revision ID: 0001
Revises: 
Create Date: 2026-05-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('is_bot', sa.Boolean(), nullable=True),
                    sa.Column('refer_id', sa.Integer(), nullable=True),
                    sa.Column('first_name', sa.String(
                        length=255), nullable=False),
                    sa.Column('last_name', sa.String(
                        length=255), nullable=True),
                    sa.Column('username', sa.String(
                        length=255), nullable=True),
                    sa.Column('language_code', sa.String(
                        length=10), nullable=True),
                    sa.Column('is_premium', sa.Boolean(), nullable=True),
                    sa.Column('can_join_groups', sa.Boolean(), nullable=True),
                    sa.Column('can_read_all_groups_messages',
                              sa.Boolean(), nullable=True),
                    sa.Column('supports_inline_queries',
                              sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('blocked_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    if_not_exists=True,
                    )
    op.create_index('idx_users_username', 'users', [
                    'username'], unique=False, if_not_exists=True)
    op.create_index('idx_users_telegram_id', 'users', [
                    'id'], unique=False, if_not_exists=True)
    op.create_index('idx_users_created_at', 'users', [
                    'created_at'], unique=False, if_not_exists=True)

    op.create_table('drink_records',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('drink_name', sa.String(
                        length=255), nullable=False),
                    sa.Column('amount', sa.Float(), nullable=True),
                    sa.Column('amount_unit', sa.String(
                        length=50), nullable=True),
                    sa.Column('price', sa.Float(), nullable=True),
                    sa.Column('note', sa.String(length=500), nullable=True),
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('idx_drink_user_id', 'drink_records', [
        'user_id'], unique=False, if_not_exists=True)
    op.create_index('idx_drink_user_created', 'drink_records', [
        'user_id', 'created_at'], unique=False, if_not_exists=True)
    op.create_index('idx_drink_created_at', 'drink_records', [
        'created_at'], unique=False, if_not_exists=True)


def downgrade() -> None:
    op.drop_index('idx_drink_created_at', table_name='drink_records')
    op.drop_index('idx_drink_user_created', table_name='drink_records')
    op.drop_index('idx_drink_user_id', table_name='drink_records')
    op.drop_table('drink_records')

    op.drop_index('idx_users_created_at', table_name='users')
    op.drop_index('idx_users_telegram_id', table_name='users')
    op.drop_index('idx_users_username', table_name='users')
    op.drop_table('users')
