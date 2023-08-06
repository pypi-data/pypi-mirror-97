"""Adds alarm_active field to tags

Revision ID: 720d3e9a9af0
Revises: fa1582c9a701
Create Date: 2021-02-10 16:08:32.143061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '720d3e9a9af0'
down_revision = 'fa1582c9a701'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE tags ADD COLUMN alarm_active bool;")


def downgrade():
    op.execute("ALTER TABLE tags DROP COLUMN alarm_active;")
