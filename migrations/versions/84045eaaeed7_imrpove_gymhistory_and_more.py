"""add deployment_time, cp_now, trainer_level, total_cp, indexes and gym_history_defenders

Revision ID: 84045eaaeed7
Revises: 5afaec120529
Create Date: 2018-02-18 15:29:22.251893

"""
from alembic import op
import sqlalchemy as sa
import sys
from pathlib import Path
monocle_dir = str(Path(__file__).resolve().parents[2])
if monocle_dir not in sys.path:
    sys.path.append(monocle_dir)
from monocle import db as db

# revision identifiers, used by Alembic.
revision = '84045eaaeed7'
down_revision = '5afaec120529'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('ix_sightings_updated', 'sightings', ['updated'], unique=False)
    op.create_index('ix_sightings_spawn_id', 'sightings', ['spawn_id'], unique=False)
    op.create_index('ix_sightings_pokemon_id', 'sightings', ['pokemon_id'], unique=False)
    op.create_index('ix_sightings_lat_lon', 'sightings', ['lat', 'lon'], unique=False)
    op.create_unique_constraint('external_id_unique', 'gym_defenders', ['external_id'])
    op.add_column('gym_defenders', sa.Column('deployment_time', sa.Integer(), nullable=True))
    op.add_column('gym_defenders', sa.Column('cp_now', sa.Integer(), nullable=True))
    op.add_column('gym_defenders', sa.Column('owner_level', sa.SmallInteger(), nullable=True))
    op.add_column('fort_sightings', sa.Column('total_cp', sa.SmallInteger(), nullable=True))
    op.alter_column('gym_defenders', 'fort_id', existing_type=sa.Integer(), existing_nullable=False, nullable=True)
    op.create_table('gym_history_defenders',
       sa.Column('id', db.PRIMARY_HUGE_TYPE, nullable=False),
       sa.Column('fort_id', sa.Integer(), nullable=False),
       sa.Column('defender_id', db.UNSIGNED_HUGE_TYPE, nullable=True),
       sa.Column('date', sa.Integer(), nullable=False),
       sa.Column('created', sa.Integer(), nullable=False),
       sa.Column('cp', sa.SmallInteger(), nullable=False),
       sa.PrimaryKeyConstraint('id'),
       sa.ForeignKeyConstraint(['fort_id'], ['forts.id'], onupdate='CASCADE', ondelete='CASCADE'),
       sa.ForeignKeyConstraint(['defender_id'], ['gym_defenders.external_id'], onupdate='CASCADE', ondelete='CASCADE'),
       sa.UniqueConstraint('fort_id', 'defender_id', 'date', name='fort_id_defender_id_date')
    )

def downgrade():
    op.drop_index('ix_sightings_lat_lon', table_name='sightings')
    op.drop_index('ix_sightings_pokemon_id', table_name='sightings')
    op.drop_index('ix_sightings_spawn_id', table_name='sightings')
    op.drop_index('ix_sightings_updated', table_name='sightings')
    op.drop_constraint('external_id_unique', 'gym_defenders')
    op.drop_column('gym_defenders', 'deployment_time')
    op.drop_column('gym_defenders', 'cp_now')
    op.drop_column('gym_defenders', 'owner_level')
    op.drop_column('fort_sightings', 'total_cp')
    op.alter_column('gym_defenders', 'fort_id', existing_nullable=True, nullable=False)
    op.drop_table('gym_history_defenders')
