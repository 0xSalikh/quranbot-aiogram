"""Init.

Revision ID: 4bb4b4f8ed92
Revises:
Create Date: 2022-08-23 16:06:46.993475

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4bb4b4f8ed92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'admin_messages',
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('text', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('key'),
    )
    op.create_table(
        'cities',
        sa.Column('city_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('city_id'),
    )
    op.create_table(
        'files',
        sa.Column('file_id', sa.String(), nullable=False),
        sa.Column('telegram_file_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('file_id'),
    )
    op.create_table(
        'prayer_days',
        sa.Column('date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('date'),
    )
    op.create_table(
        'prayers_at_user_groups',
        sa.Column('prayers_at_user_group_id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('prayers_at_user_group_id'),
    )
    op.create_table(
        'suras',
        sa.Column('sura_id', sa.Integer(), nullable=False),
        sa.Column('link', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('sura_id'),
    )
    op.create_table(
        'ayats',
        sa.Column('ayat_id', sa.Integer(), nullable=False),
        sa.Column('public_id', sa.String(), nullable=False),
        sa.Column('sura_id', sa.Integer(), nullable=False),
        sa.Column('audio_id', sa.String(), nullable=False),
        sa.Column('ayat_number', sa.String(length=10), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('arab_text', sa.String(), nullable=False),
        sa.Column('transliteration', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['audio_id'],
            ['files.file_id'],
        ),
        sa.ForeignKeyConstraint(
            ['sura_id'],
            ['suras.sura_id'],
        ),
        sa.PrimaryKeyConstraint('ayat_id'),
    )
    op.create_table(
        'podcasts',
        sa.Column('podcast_id', sa.String(), nullable=False),
        sa.Column('file_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ['file_id'],
            ['files.file_id'],
        ),
        sa.PrimaryKeyConstraint('podcast_id'),
    )
    op.create_table(
        'prayers',
        sa.Column('prayer_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('time', sa.Time(), nullable=False),
        sa.Column('city_id', sa.String(), nullable=True),
        sa.Column('day_id', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ['city_id'],
            ['cities.city_id'],
        ),
        sa.ForeignKeyConstraint(
            ['day_id'],
            ['prayer_days.date'],
        ),
        sa.PrimaryKeyConstraint('prayer_id'),
    )
    op.create_table(
        'users',
        sa.Column('chat_id', sa.Integer(), nullable=False),
        sa.Column(
            'is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False,
        ),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('day', sa.Integer(), nullable=True),
        sa.Column('city_id', sa.String(), nullable=True),
        sa.Column('referrer_id', sa.Integer(), nullable=True),
        sa.Column('legacy_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['city_id'],
            ['cities.city_id'],
        ),
        sa.ForeignKeyConstraint(
            ['referrer_id'],
            ['users.chat_id'],
        ),
        sa.PrimaryKeyConstraint('chat_id'),
    )
    op.create_table(
        'favorite_ayats',
        sa.Column('ayat_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['ayat_id'],
            ['ayats.ayat_id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.chat_id'],
        ),
        sa.PrimaryKeyConstraint('ayat_id', 'user_id'),
    )
    op.create_table(
        'prayers_at_user',
        sa.Column('prayer_at_user_id', sa.Integer(), nullable=False),
        sa.Column('public_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('prayer_id', sa.String(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.Column('prayer_group_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ['prayer_group_id'],
            ['prayers_at_user_groups.prayers_at_user_group_id'],
        ),
        sa.ForeignKeyConstraint(
            ['prayer_id'],
            ['prayers.prayer_id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.chat_id'],
        ),
        sa.PrimaryKeyConstraint('prayer_at_user_id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prayers_at_user')
    op.drop_table('favorite_ayats')
    op.drop_table('users')
    op.drop_table('prayers')
    op.drop_table('podcasts')
    op.drop_table('ayats')
    op.drop_table('suras')
    op.drop_table('prayers_at_user_groups')
    op.drop_table('prayer_days')
    op.drop_table('files')
    op.drop_table('cities')
    op.drop_table('admin_messages')
    # ### end Alembic commands ###
