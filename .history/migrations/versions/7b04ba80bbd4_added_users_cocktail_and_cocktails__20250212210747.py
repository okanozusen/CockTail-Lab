 """Added users_cocktail and cocktails tables cleanly

Revision ID: 7b04ba80bbd4
Revises: e8e2d4d0400f
Create Date: 2025-02-12 21:02:26.137485

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7b04ba80bbd4'
down_revision = 'e8e2d4d0400f'
branch_labels = None
depends_on = None


def upgrade():
    """Create users_cocktail and cocktails tables."""
    op.create_table('users_cocktail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=128), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

    op.create_table('cocktails',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('cup', sa.String(), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('ingredients', sa.JSON(), nullable=False),
        sa.Column('color', sa.String(), nullable=False),
        sa.Column('sweetness', sa.Float(), nullable=True),
        sa.Column('bitterness', sa.Float(), nullable=True),
        sa.Column('smoothness', sa.Float(), nullable=True),
        sa.Column('strength', sa.Float(), nullable=True),
        sa.Column('freshness', sa.Float(), nullable=True),
        sa.Column('enjoyment_rating', sa.Float(), nullable=True),
        sa.Column('final_strength', sa.Float(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users_cocktail.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    """Remove only users_cocktail and cocktails tables (DO NOT TOUCH Gaming Lab)."""
    op.drop_table('cocktails')
    op.drop_table('users_cocktail')
