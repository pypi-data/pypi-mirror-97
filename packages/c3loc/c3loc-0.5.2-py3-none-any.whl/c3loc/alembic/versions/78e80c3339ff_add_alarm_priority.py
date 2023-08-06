"""Add alarm priority

Revision ID: 78e80c3339ff
Revises: 5ccf897e51af
Create Date: 2020-12-02 14:22:02.925553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78e80c3339ff'
down_revision = '5ccf897e51af'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE alarms ADD COLUMN priority integer default 0;')
    pass


def downgrade():
    op.execute('ALTER TABLE alarms DROP COLUMN priority;')
    pass
