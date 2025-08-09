# backend/alembic/script.py.mako
"""rename_metadata_column

Revision ID: 74bd91903af3
Revises: 001
Create Date: 2025-08-08 18:11:10.851844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74bd91903af3'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename metadata column to event_metadata
    op.alter_column('activity_events', 'metadata', new_column_name='event_metadata')


def downgrade() -> None:
    # Rename event_metadata column back to metadata
    op.alter_column('activity_events', 'event_metadata', new_column_name='metadata')
