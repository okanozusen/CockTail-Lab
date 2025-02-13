"""Added users_cocktail and cocktails tables cleanly

Revision ID: 7b04ba80bbd4
Revises: e8e2d4d0400f
Create Date: 2025-02-12 21:02:26.137485

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7b04ba80bbd4'
down_revision = 'e8e2d4d0400f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    sa.ForeignKeyConstraint(['user_id'], ['users_cocktail.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('replies')
    op.drop_table('users')
    op.drop_table('friends')
    op.drop_table('games')
    op.drop_table('messages')
    op.drop_table('knex_migrations_lock')
    op.drop_table('knex_migrations')
    op.drop_table('posts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('posts_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('game_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('profile_pic', sa.TEXT(), server_default=sa.text("'https://placehold.co/50'::text"), autoincrement=False, nullable=True),
    sa.Column('username', sa.TEXT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='posts_user_id_foreign', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='posts_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('knex_migrations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('batch', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('migration_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='knex_migrations_pkey')
    )
    op.create_table('knex_migrations_lock',
    sa.Column('index', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_locked', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('index', name='knex_migrations_lock_pkey')
    )
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sender', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('receiver', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )
    op.create_table('games',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('release_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='games_pkey')
    )
    op.create_table('friends',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('friend_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], name='friends_friend_id_foreign', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='friends_user_id_foreign', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='friends_pkey'),
    sa.UniqueConstraint('user_id', 'friend_id', name='friends_user_id_friend_id_unique')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('profile_pic', sa.VARCHAR(length=255), server_default=sa.text('NULL::character varying'), autoincrement=False, nullable=True),
    sa.Column('banner', sa.VARCHAR(length=255), server_default=sa.text('NULL::character varying'), autoincrement=False, nullable=True),
    sa.Column('bio', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('platforms', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=True),
    sa.Column('genres', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_unique'),
    sa.UniqueConstraint('username', name='users_username_unique'),
    postgresql_ignore_search_path=False
    )
    op.create_table('replies',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('username', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='replies_post_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='replies_pkey')
    )
    op.drop_table('cocktails')
    op.drop_table('users_cocktail')
    # ### end Alembic commands ###
