"""empty message

Revision ID: b095d75323f6
Revises: c106e9a6180f
Create Date: 2020-06-13 22:55:29.430817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b095d75323f6'
down_revision = 'c106e9a6180f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('acontact',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('artist_id')
    )
    op.create_table('agenres',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('genres', sa.ARRAY(sa.String()), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('artist_id')
    )
    op.create_table('aimage',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('image_link', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('artist_id')
    )
    op.create_table('alocation',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('artist_id')
    )
    op.create_table('aseek',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('seeking', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('artist_id')
    )
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcontact',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('venue_id')
    )
    op.create_table('vgenres',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('genres', sa.ARRAY(sa.String()), nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('venue_id')
    )
    op.create_table('vimage',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('image_link', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('venue_id')
    )
    op.create_table('vlocation',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('venue_id')
    )
    op.create_table('vseek',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('seeking', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('venue_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vseek')
    op.drop_table('vlocation')
    op.drop_table('vimage')
    op.drop_table('vgenres')
    op.drop_table('vcontact')
    op.drop_table('show')
    op.drop_table('aseek')
    op.drop_table('alocation')
    op.drop_table('aimage')
    op.drop_table('agenres')
    op.drop_table('acontact')
    op.drop_table('venue')
    op.drop_table('artist')
    # ### end Alembic commands ###
