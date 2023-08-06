import asyncio
from uuid import UUID
import struct

from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.exceptions import InvalidSignature

from ..config import CONFIG
from .frame import Frame, InvalidFrame
from ..proto.common_pb2 import ListenerID
from ..proto.location_pb2 import IBeaconSummary, TempBeaconSummary, LABeaconSummary
from ..proto.secbeacon_pb2 import SecureSmartRelay

class PacketType:
    """Enum emulation class."""

    ID = 0
    DATA = 1
    SECURE = 2
    RESPONSE = 3
    REQUEST = 4
    ID_REQUEST = 5
    HEALTH_CHECK = 6
    TEMPBEACON = 7
    LABEACON = 8
    SSR = 9


def batt_2032_pct(mvolts):
    batt_pct = 0

    if mvolts >= 3000:
        batt_pct = 100
    elif mvolts > 2900:
        batt_pct = 100 - ((3000 - mvolts) * 58) / 100
    elif mvolts > 2740:
        batt_pct = 42 - ((2900 - mvolts) * 24) / 160
    elif mvolts > 2440:
        batt_pct = 18 - ((2740 - mvolts) * 12) / 300
    elif mvolts > 2100:
        batt_pct = 6 - ((2440 - mvolts) * 6) / 340
    return batt_pct


def valid_ssr(ssr):
    key = CONFIG['SSR_KEY']
    c = cmac.CMAC(algorithms.AES(key))
    c.update(ssr.payload)
    calculated = c.finalize()
    if calculated[:4] == ssr.mac:
        return True
    # print(calculated, ssr.payload.hex(), ssr.mac.hex())
    return False


class ListenerProtocol(object):
    callback = None
    db_pool = None

    def __init__(self, verbose=False):
        self._rx_buf = bytearray()
        self.transport = None
        self._frame = Frame()
        self.verbose = verbose
        if not self.db_pool:
            raise NotImplementedError("ListenerProtocol.db_pool must be set before instantiation")
        self.router = {
            PacketType.DATA: self.process_ibeacon,
            PacketType.LABEACON: self.process_relay_beacon,
            PacketType.SSR: self.process_ssr,
        }
        self.ignored_types = {PacketType.HEALTH_CHECK, PacketType.SECURE, PacketType.TEMPBEACON}
        self._l_id = None
        self.listener_id = None
        self.peer_name = None

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.peer_name = transport.get_extra_info('peername')[0]
        print("Connection from {}".format(self.peer_name))

    def eof_received(self):
        pass

    def data_received(self, data: bytes) -> None:
        try:
            self._frame.add_bytes(data)
        except InvalidFrame as e:
            print(f"Error: {self.peer_name} sent an InvalidFrame: {e.args[0]}. Disconnecting")
            self.transport.close()
            return
        for msg in self._frame.get_messages():
            loop = asyncio.get_event_loop()
            loop.create_task(self.process_packet(msg))

    def _print_reason(self, report):
        print("\t\tReason: {}".format(self._reason(report)))

    def _reason(self, report):
        reason = ""
        if report.reason in [IBeaconSummary.IBeaconReport.EventReason.ENTRY,
            TempBeaconSummary.TempBeaconReport.EventReason.ENTRY,
                             LABeaconSummary.LABeaconReport.EventReason.ENTRY]:
            reason = "ENTRY"
        if report.reason in [IBeaconSummary.IBeaconReport.EventReason.MOVE,
                             TempBeaconSummary.TempBeaconReport.EventReason.MOVE,
                             LABeaconSummary.LABeaconReport.EventReason.MOVE]:
            reason = "MOVE"
        if report.reason in [IBeaconSummary.IBeaconReport.EventReason.STATUS,
                             TempBeaconSummary.TempBeaconReport.EventReason.STATUS,
                             LABeaconSummary.LABeaconReport.EventReason.STATUS]:
            reason = "STATUS"
        if report.reason in [IBeaconSummary.IBeaconReport.EventReason.EXIT,
                             TempBeaconSummary.TempBeaconReport.EventReason.EXIT,
                             LABeaconSummary.LABeaconReport.EventReason.EXIT]:
            reason = "EXIT"
        return reason

    async def _upsert_listener(self, conn):
        await conn.execute('INSERT into listeners (id) VALUES ($1) '
                           'ON CONFLICT ON CONSTRAINT listeners_pkey '
                           'DO UPDATE SET last_seen = (now() at time zone \'utc\')',
                           self.listener_id)
        # Add a default zone for listeners
        zone_id = await self._select_zone_id(conn)
        if not zone_id:
            r = await conn.fetchrow('INSERT INTO zones (name) VALUES ($1) RETURNING id',
                                          f'Near Listener {self.listener_id}')
            zone_id = r[0]
            await conn.execute('UPDATE listeners SET zone_id = $1 WHERE id = $2',
                               zone_id, self.listener_id)

    async def _select_zone_id(self, conn):
        l = await conn.fetchrow('SELECT zone_id FROM listeners WHERE id = $1', self.listener_id)
        if not l:
            return None
        return l[0]

    async def process_packet(self, msg):
        if msg.type == PacketType.ID:
            self.process_id(msg)
            return

        if not self.listener_id:
            print(f"Error: {self.peer_name} attempted non-ID packet before ID. Dropping connection")
            self.transport.close()
            return

        if msg.type in self.ignored_types:
            return

        conn = await self.db_pool.acquire()
        await self._upsert_listener(conn)  # Ensures listener in db and/or updates last_seen
        if msg.type not in self.router:
            print(f"Warning: No implementation for packet type: {msg.type}")
            return
        await self.router[msg.type](msg, conn)
        await self.db_pool.release(conn)

    def process_id(self, msg):
        l_id = ListenerID()
        l_id.ParseFromString(msg.data)
        self._l_id = l_id.listener_id
        self.listener_id = self._l_id.hex()
        print("{} identified as {} (version {})".format(
            self.peer_name, self._l_id.hex(), l_id.version))

    async def process_ibeacon(self, msg, conn):
        data = IBeaconSummary()
        data.ParseFromString(msg.data)

        # Convert to upsert when last_seen field is added?
        tag_upsert = await conn.prepare('INSERT into tags (uuid, major, minor, type)'
                                        'VALUES ($1, $2, $3, $4) ON CONFLICT ON CONSTRAINT uk_ibeacon '
                                        'DO UPDATE SET last_seen = (now() at time zone \'utc\')')
        tag_select = await conn.prepare('SELECT id FROM tags WHERE uuid = $1 AND major = $2 AND minor = $3')
        ibeacon_log = await conn.prepare('INSERT into log '
                                         '(tag_id, zone_id, listener_id, distance, variance, reason)'
                                         'VALUES ($1, $2, $3, $4, $5, $6)')
        listener_zone = await self._select_zone_id(conn)
        for b in data.reports:
            uuid = UUID(bytes=b.uuid)
            tag_type = ''
            if uuid == CONFIG['LA_UUID']:
                tag_type = 'LocationAnchor'
            else:
                tag_type = 'iBeacon'
            await tag_upsert.fetch(uuid, b.major_num, b.minor_num, tag_type)
            t = await tag_select.fetchrow(uuid, b.major_num, b.minor_num)
            await ibeacon_log.fetch(t['id'], listener_zone, self.listener_id, b.distance_cm/100,
                                    round(b.variance/2000, 1), self._reason(b))

    async def process_ssr(self, msg, conn):
        data = SecureSmartRelay()
        data.ParseFromString(msg.data)
        if not valid_ssr(data):
            print("Invalid SSR, MAC check failed")
            return

        if len(data.payload) < 12:
            print("Ignoring short (but valid MAC?) SSR packet")
            return

        (rssi1m, b_id, ts, status) = struct.unpack("<bIIB", data.payload[2:12])
        batt = status >> 1
        button = bool(status & 0x1)
        
        row = await conn.fetchrow(
            'INSERT into tags (bid, type, battery_pct, alarm_active, last_clock) '
            'VALUES ($1, $2, $3, $4, $5) ON CONFLICT ON CONSTRAINT tags_bid_key DO '
            'UPDATE SET battery_pct = excluded.battery_pct, alarm_active = excluded.alarm_active, '
            'last_clock = excluded.last_clock '
            'WHERE tags.last_clock < excluded.last_clock RETURNING tags.id',
            b_id, "SecureSmartRelay", batt, button, ts)
        
        if not row:
            # print(f"Skipping duplicate or replayed packet for SSR {b_id}")
            return
        (t_id,) = row

        # Service the alarm state
        if button:
            row = await conn.fetchrow("SELECT id from alarms WHERE tag_id = $1 and acknowledged = FALSE;", t_id)
            if not row:
                await conn.fetchrow('INSERT INTO alarms (tag_id) VALUES ($1)', t_id)
            else:
                row = await conn.fetchrow('UPDATE alarms SET last_ts = now() WHERE id = $1 AND acknowledged = FALSE',
                                          row[0])

        (anchor_id, anchor_delta, anchor_dist) = (None, None, None)
        azone_id = a_db_id = None
        if len(data.payload) == 18 and data.payload[1] in (0x0, 0x1):  # SSRv0
            (anchor_id, anchor_delta, anchor_dist) = struct.unpack(
                "<IBB", data.payload[12:])
            anchor_dist = anchor_dist / 10
        elif len(data.payload) == 19 and data.payload[1] == 0x2:  # SSRv1
            (anchor_id, anchor_delta, anchor_rssi, anchor_cal) = struct.unpack(
                "<IBBB", data.payload[12:])
            anchor_dist = 10 ** ((anchor_cal - anchor_rssi) / (10 * 3.2))

        if anchor_id:
            # Anchor upsert
            (a_db_id, azone_id) = await conn.fetchrow('INSERT into tags (bid, type) '
                             'VALUES ($1, $2) ON CONFLICT ON CONSTRAINT tags_bid_key '
                             'DO UPDATE SET last_seen = (now() at time zone \'utc\') RETURNING id, zone_id',
                             anchor_id, "SecureLocationAnchor")
            if not azone_id:
                # Create default zone for anchor if nonexistant
                (azone_id,) = await conn.fetchrow('INSERT INTO zones (name) VALUES ($1) RETURNING id',
                                        f'Near SLA {b_id}')
                await conn.execute('UPDATE tags SET zone_id = $1 WHERE id = $2',
                                   azone_id, a_db_id)

        await conn.fetch('INSERT into log '
                           '(tag_id, zone_id, listener_id, distance,'
                           'variance, anchor_id, anchor_dist, anchor_ts_delta, reason)'
                           'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
                         t_id, azone_id, self.listener_id, data.distance_cm / 100,
                         round(data.variance / 2000, 1), a_db_id, anchor_dist, anchor_delta, None)


    async def process_relay_beacon(self, msg, conn):
        data = LABeaconSummary()
        data.ParseFromString(msg.data)
        # Convert to upsert when last_seen field is added?
        tag_upsert = await conn.prepare('INSERT into tags (mac, type)'
                                        'VALUES ($1, $2) ON CONFLICT ON CONSTRAINT uk_mac '
                                        'DO UPDATE SET last_seen = (now() at time zone \'utc\'), battery_pct = $3,'
                                        'alarm_active = $4')
        tag_select = await conn.prepare('SELECT id FROM tags WHERE mac = $1')
        anchor_upsert = await conn.prepare('INSERT into tags (uuid, major, minor, type) '
                                           'VALUES ($1, $2, $3, $4) ON CONFLICT ON CONSTRAINT uk_ibeacon '
                                           'DO UPDATE SET last_seen = (now() at time zone \'utc\') RETURNING id, zone_id')
        anchor_select = await conn.prepare('SELECT id, zone_id FROM tags WHERE uuid = $1 AND major = $2 AND minor = $3')
        labeacon_log = await conn.prepare('INSERT into log '
                                          '(tag_id, zone_id, listener_id, distance,'
                                          'variance, anchor_id, anchor_dist, anchor_ts_delta, reason)'
                                          'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)')
        alarm_update = await conn.prepare('UPDATE alarms SET last_ts = now() '
                                          'WHERE tag_id = $1 AND acknowledged = FALSE '
                                          'RETURNING id')
        listener_zone = await self._select_zone_id(conn)
        for b in data.reports:
            b_id = bytes(reversed(b.beacon_id)).hex()
            await tag_upsert.fetch(b_id, 'SmartRelay', b.battery_pct if b.battery_pct > 0 else None,
                                   b.status == LABeaconSummary.LABeaconReport.ButtonStatus.PRESSED)
            t = await tag_select.fetchrow(b_id)

            # Service alarm
            if b.status == LABeaconSummary.LABeaconReport.ButtonStatus.PRESSED:
                alarm = await alarm_update.fetchrow(t['id'])
                if not alarm:
                    await conn.fetch('INSERT INTO alarms (tag_id) VALUES ($1)', t['id'])

            if b.nearest == 0 and b.nearest_delta == 0 and b.nearest_dist == 0:
                # No current anchor
                await labeacon_log.fetch(
                    t['id'], listener_zone, self.listener_id, b.distance_cm / 100,
                    round(b.variance / 2000, 1), None, None, None, self._reason(b))
                continue
            # Reconstruct the iBeacon from the LA data
            major = b.nearest >> 16
            minor = b.nearest & 0xffff
            r = await anchor_upsert.fetchrow(CONFIG['LA_UUID'], major, minor, 'LocationAnchor')
            a_id, azone_id = r[0], r[1]
            if not azone_id:
                s = await conn.fetchrow('INSERT INTO zones (name) VALUES ($1) RETURNING id',
                                        f'Near LA {major}:{minor}')
                azone_id = s[0]
                await conn.execute('UPDATE tags SET zone_id = $1 WHERE id = $2',
                                   azone_id, a_id)
            anchor = await anchor_select.fetchrow(CONFIG['LA_UUID'], major, minor)
            await labeacon_log.fetch(
                t['id'], anchor['zone_id'], self.listener_id, b.distance_cm / 100, round(b.variance / 2000, 1),
                anchor['id'], b.nearest_dist/10, b.nearest_delta, self._reason(b))

    async def process_health_check(self, msg, conn):
        pass

    def error_received(self, exc: Exception) -> None:
        print(f'Error received: {exc}')

    def connection_lost(self, exc: Exception) -> None:
        print("{} has disconnected".format(self.peer_name))
