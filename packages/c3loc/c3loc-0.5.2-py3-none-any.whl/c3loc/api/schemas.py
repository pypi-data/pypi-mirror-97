import json
import string

from marshmallow import Schema, fields, validates


class JsonField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value:
            return json.loads(value)
        return {}

    def _deserialize(self, value, attr, data, **kwargs):
        return value


class AttrsMixin:
    attrs = JsonField(allow_none=True, default={})


class ListenerSchema(Schema, AttrsMixin):
    id = fields.Str(dump_only=True)
    name = fields.Str(allow_none=True)
    zone_id = fields.Int(allow_none=True)
    last_seen = fields.DateTime(dump_only=True)


class ZoneSchema(Schema, AttrsMixin):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GroupSchema(Schema, AttrsMixin):
    id = fields.Int(dump_only=True)
    name = fields.Str()


def validate_mac(value):
    valid_char = set(string.hexdigits)
    valid_char.add(':')
    return all(c in set(valid_char) for c in value)


class MacMixin:
    mac = fields.Str(validate=validate_mac)


class RequiredMacMixin:
    mac = fields.Str(required=True, validate=validate_mac)


class TagPatchSchema(Schema, AttrsMixin):
    name = fields.Str(allow_none=True)
    zone_id = fields.Int(allow_none=True, validate=lambda x: x > 0)
    group_id = fields.Int(allow_none=True, validate=lambda x: x > 0)


class TagCreateBase(Schema, AttrsMixin):
    id = fields.Int(dump_only=True)
    name = fields.Str(allow_none=True)
    zone_id = fields.Int(allow_none=True)
    group_id = fields.Int(allow_none=True)
    last_seen = fields.DateTime(dump_only=True)
    type = fields.Str(required=True, validate=lambda x: x in {
        'iBeacon', 'SmartRelay', 'LocationAnchor', 'SecureLocationAnchor', 'SecureSmartRelay'})
    battery_pct = fields.Int(allow_none=True)
    alarm_active = fields.Boolean(allow_none=True)


class iBeaconTagMixin:
    uuid = fields.UUID(required=True)
    major = fields.Int(required=True, validate=lambda x: x >= 0 < (2 ** 16))
    minor = fields.Int(required=True, validate=lambda x: x >= 0 < (2 ** 16))


class SecureBeaconTagMixin:
    bid = fields.Int(required=True)


class MacBeaconTagMixin(RequiredMacMixin):
    pass


class SecureBeaconCreateSchema(TagCreateBase, SecureBeaconTagMixin):
    pass


class iBeaconCreateSchema(TagCreateBase, iBeaconTagMixin):
    pass


class MacBeaconCreateSchema(TagCreateBase, MacBeaconTagMixin):
    pass


class ProxLinks(Schema):
    tag = fields.URL(required=True)
    zone = fields.URL(required=True)


class ProxSchema(Schema):
    tag_id = fields.Int(required=True)
    tag_name = fields.Str(required=True)
    distance = fields.Float(required=True)
    zone_name = fields.Str(required=True)
    last_seen = fields.DateTime(required=True)
    tag_type = fields.Str(required=True)
    alarm_active = fields.Str(required=True)
    links = fields.Nested(ProxLinks)


class AlarmLinks(Schema):
    tag = fields.URL(required=True)
    zone = fields.URL(required=True)


class AlarmSchema(Schema):
    id = fields.Int(required=True)
    tag_name = fields.Str(required=True)
    zone_name = fields.Str(required=True)
    start_ts = fields.DateTime(required=True)
    last_ts = fields.DateTime(required=True)
    acknowledged = fields.Boolean(required=True)
    priority = fields.Int(required=True)
    links = fields.Nested(AlarmLinks)


class AlarmPatch(Schema):
    acknowledged = fields.Boolean(required=True)


class HistorySchema(Schema):
    ts = fields.DateTime(required=True)
    zone_id = fields.Int(required=True)
    zone_name = fields.Str(required=True)
    distance_cm = fields.Float(required=True)


listeners_schema = ListenerSchema(many=True)
listener_schema = ListenerSchema()

zones_schema = ZoneSchema(many=True)
zone_schema = ZoneSchema()
groups_schema = GroupSchema(many=True)
group_schema = GroupSchema()

ibeacon_post_schema = iBeaconCreateSchema()
macbeacon_post_schema = MacBeaconCreateSchema()
secure_beacon_post_schema = SecureBeaconCreateSchema()
tag_patch_schema = TagPatchSchema()

prox_schema = ProxSchema(many=True)

alarm_schema = AlarmSchema()
alarms_schema = AlarmSchema(many=True)
alarm_patch_schema = AlarmPatch()

history_schema = HistorySchema(many=True)
