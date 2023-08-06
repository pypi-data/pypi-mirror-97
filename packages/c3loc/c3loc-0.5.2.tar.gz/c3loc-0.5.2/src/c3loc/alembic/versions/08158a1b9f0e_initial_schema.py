"""Initial schema

Revision ID: 08158a1b9f0e
Revises: 
Create Date: 2020-10-28 19:26:23.977822

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, MACADDR, UUID


# revision identifiers, used by Alembic.
revision = '08158a1b9f0e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE IF NOT EXISTS zones (
    id serial,
    name varchar,
    attrs jsonb,
    PRIMARY KEY(id));""")
    op.execute("""
    CREATE TABLE IF NOT EXISTS groups (
    id serial,
    name varchar,
    attrs jsonb,
    PRIMARY KEY(id));""")
    op.execute("""
    CREATE TABLE IF NOT EXISTS listeners (
    id varchar not null,
    name varchar,
    zone_id int,
    last_seen timestamp without time zone DEFAULT (now() at time zone 'utc'),
    attrs jsonb,
    PRIMARY KEY(id),
    UNIQUE(name),
    CONSTRAINT fk_zone
        FOREIGN KEY(zone_id)
        REFERENCES zones(id)
        ON DELETE SET NULL);""")
    op.execute("""
    DO $$ BEGIN
    CREATE TYPE tag_type as ENUM ('iBeacon', 'SmartRelay', 'LocationAnchor');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;""")
    op.execute("""
    CREATE TABLE IF NOT EXISTS tags (
    id serial,
    name varchar,
    mac macaddr,
    uuid uuid,
    major int4,
    minor int4,
    type tag_type NOT NULL,
    attrs jsonb,
    zone_id integer,
    last_seen timestamp without time zone DEFAULT (now() at time zone 'utc'),
    group_id integer,
    PRIMARY KEY (id),
    CONSTRAINT uk_ibeacon
    UNIQUE (uuid, major, minor),
    CONSTRAINT uk_mac
    UNIQUE (mac),
    CONSTRAINT fk_zone
                  FOREIGN KEY (zone_id)
                  REFERENCES zones(id)
                  ON DELETE SET NULL,
    CONSTRAINT fk_group
                  FOREIGN KEY (group_id)
                  REFERENCES groups(id)
                  ON DELETE SET NULL
);""")
    op.execute("""
    CREATE OR REPLACE FUNCTION def_tag_name() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.name IS NOT NULL OR NEW.name != ''
       THEN RETURN NEW;
    ELSIF NEW.type = 'iBeacon' THEN
        NEW.name := 'iBeacon ' || NEW.uuid || ':' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'LocationAnchor' THEN
            NEW.name := 'Location Anchor ' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'SmartRelay' THEN
            NEW.name := 'SmartRelay ' || NEW.mac;
    END IF;
    return NEW;
END
$$;""")
    op.execute("""
    DO $$ BEGIN
    CREATE TRIGGER tags_set_def_name
    BEFORE INSERT OR UPDATE ON tags
    FOR EACH ROW
    EXECUTE PROCEDURE def_tag_name();
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;""")
    op.execute("""DO $$ BEGIN
    CREATE TYPE report_reason as ENUM ('ENTRY', 'MOVE', 'STATUS', 'EXIT');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;""")
    op.execute("""DO $$ BEGIN
    CREATE TYPE report_reason as ENUM ('ENTRY', 'MOVE', 'STATUS', 'EXIT');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;""")
    op.execute("""CREATE TABLE IF NOT EXISTS log (
    tag_id int,
    zone_id int,
    ts timestamp without time zone default (now() at time zone 'utc'),
    distance_cm numeric(4,2),
    variance real,
    listener_id varchar,
    data jsonb,
    anchor_dist numeric(4,2),
    anchor_ts_delta int,
    anchor_id int,
    reason report_reason,
    CONSTRAINT fk_tag
                 FOREIGN KEY (tag_id)
                 REFERENCES tags(id)
                 ON DELETE CASCADE,
    CONSTRAINT fk_zone
                 FOREIGN KEY (zone_id)
                 REFERENCES zones(id)
                 ON DELETE SET NULL,
    CONSTRAINT fk_anchor
                 FOREIGN KEY (anchor_id)
                 REFERENCES tags(id)
                 ON DELETE SET NULL,
    CONSTRAINT fk_listener
                 FOREIGN KEY (listener_id)
                 REFERENCES listeners(id)
                 ON DELETE SET NULL
);""")
    op.execute("CREATE INDEX IF NOT EXISTS idx_log_tag_id ON log (tag_id);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_log_anchor_id ON log (anchor_id);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_log_zone_id ON log (zone_id);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_log_ts ON log (ts DESC);")


def downgrade():
    pass
