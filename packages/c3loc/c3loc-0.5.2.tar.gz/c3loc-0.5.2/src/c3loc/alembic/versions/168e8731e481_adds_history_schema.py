"""adds history schema

Revision ID: 168e8731e481
Revises: 78e80c3339ff
Create Date: 2020-12-18 15:50:07.278444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '168e8731e481'
down_revision = '78e80c3339ff'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""CREATE TABLE IF NOT EXISTS history (
    tag_id int,
    zone_id int,
    zone_name varchar,
    ts timestamp without time zone default (now() at time zone 'utc'),
    distance numeric(4,2),
    CONSTRAINT fk_tag FOREIGN KEY (tag_id)
    REFERENCES tags(id) ON DELETE CASCADE,
    CONSTRAINT fk_zone FOREIGN KEY (zone_id)
    REFERENCES zones(id) ON DELETE SET NULL);""")

    op.execute("""CREATE FUNCTION append_history()
    RETURNS TRIGGER
    LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO history (tag_id, zone_id, ts, distance, zone_name)
    VALUES (OLD.id, OLD.zone_id, OLD.last_seen, OLD.distance,
            (SELECT zones.name from zones where zones.id = OLD.zone_id));
    RETURN NEW;
END;
$$""")
    op.execute("""CREATE TRIGGER tags_update_zone
    AFTER UPDATE OF zone_id ON tags FOR EACH ROW
    WHEN (OLD.zone_id IS DISTINCT FROM NEW.zone_id AND OLD.zone_id IS NOT NULL)
    EXECUTE PROCEDURE append_history();""")
    op.execute("ALTER TABLE log RENAME distance_cm TO distance;")
    op.execute("ALTER TABLE tags RENAME distance_cm TO distance")


def downgrade():
    op.execute("DROP FUNCTION append_history CASCADE;")
    op.execute("DROP TABLE IF EXISTS history;")
    op.execute("ALTER TABLE log RENAME distance TO distance_cm")
    op.execute("ALTER TABLE tags RENAME distance TO distance_cm")
