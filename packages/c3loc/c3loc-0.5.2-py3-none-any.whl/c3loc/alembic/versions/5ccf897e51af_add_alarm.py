"""Add alarm

Revision ID: 5ccf897e51af
Revises: 08158a1b9f0e
Create Date: 2020-10-31 12:47:09.284114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ccf897e51af'
down_revision = '08158a1b9f0e'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""CREATE TABLE alarms (
    id serial,
    tag_id integer not null,
    start_ts timestamp without time zone default CURRENT_TIMESTAMP,
    last_ts timestamp without time zone default CURRENT_TIMESTAMP,
    ack_ts timestamp without time zone default NULL,
    acknowledged boolean generated always as ( ack_ts IS NOT NULL ) STORED,
    PRIMARY KEY (id),
    CONSTRAINT fk_tag FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    );""")
    op.execute('ALTER TABLE tags ADD COLUMN battery_pct integer;')
    op.execute('ALTER TABLE tags ADD COLUMN distance_cm numeric(4,2);')


def downgrade():
    op.drop_table('alarms')
    op.execute('ALTER TABLE tags DROP COLUMN battery_pct')
    op.execute('ALTER TABLE tags DROP COLUMN distance_cm')

