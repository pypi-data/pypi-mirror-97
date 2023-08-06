"""Adds SSR/SLA

Revision ID: fa1582c9a701
Revises: 168e8731e481
Create Date: 2021-02-10 15:56:52.096102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa1582c9a701'
down_revision = '168e8731e481'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE tags ADD COLUMN bid bigint UNIQUE;")
    op.execute("ALTER TABLE tags ADD COLUMN last_clock bigint;")
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
    ELSIF New.type = 'SecureSmartRelay' THEN
            NEW.name := 'SecureSmartRelay ' || NEW.bid;
    ELSIF New.type = 'SecureLocationAnchor' THEN
            NEW.name := 'SecureLocationAnchor ' || NEW.bid;
    END IF;
    return NEW;
END
$$;""")
    op.execute("""
DO $$ BEGIN
    ALTER TYPE tag_type ADD VALUE 'SecureLocationAnchor';
    ALTER TYPE tag_type ADD VALUE 'SecureSmartRelay';
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;""")


def downgrade():
    op.execute("ALTER TABLE tags DROP COLUMN bid;")
    op.execute("ALTER TABLE tags DROP COLUMN last_clock;")
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

