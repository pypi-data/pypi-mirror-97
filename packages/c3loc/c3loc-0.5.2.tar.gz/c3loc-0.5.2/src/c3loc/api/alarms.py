import json

from aiohttp import web

from .schemas import alarms_schema, alarm_schema, alarm_patch_schema
from .views import ValidatingView, paginate_query


def process_alarm_links(result):
    zone_id = result['zone_id']
    tag_id = result['tag_id']
    d_r = dict(result)
    d_r['links'] = {
        "tag": f"/api/tags/{tag_id}",
        "zone": f"/api/zones/{zone_id}" if zone_id else None
    }
    return d_r


class AlarmsView(ValidatingView):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = None
            if 'acknowledged' in self.request.query:
                try:
                    ack_filter = int(self.request.query['acknowledged'])
                except ValueError:
                    raise web.HTTPBadRequest(reason="Invalid value for query param 'acknowledged' (should be 0 or 1)")
                query = ('SELECT alarms.id as id, tag_id, tags.name as tag_name, zones.name as zone_name, start_ts, last_ts, '
                         'acknowledged, zone_id, priority FROM alarms JOIN tags ON tag_id = tags.id '
                         'LEFT JOIN zones ON tags.zone_id = zones.id WHERE acknowledged = $1', bool(ack_filter))
            else:
                query = ('SELECT alarms.id as id, tag_id, tags.name as tag_name, zones.name as zone_name, start_ts, last_ts, '
                         'acknowledged, zone_id, priority FROM alarms JOIN tags ON tag_id = tags.id '
                         'LEFT JOIN zones ON tags.zone_id = zones.id', )
            alarms = await conn.fetch(*paginate_query(self.request, query))
            return web.json_response(alarms_schema.dump(
                [process_alarm_links(r) for r in alarms]
            ))


class AlarmView(ValidatingView):
    async def get(self):
        a_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l = await conn.fetchrow('SELECT alarms.id as id, tag_id, tags.name, zones.name as zone_name, start_ts, last_ts, '
                                    'acknowledged as tag_name, zone_id, priority FROM alarms JOIN tags ON tag_id = tags.id '
                                    'LEFT JOIN zones ON tags.zone_id = zones.id WHERE alarms.id = $1', a_id)
            if not l:
                raise web.HTTPNotFound
            return web.json_response(alarm_schema.dump(process_alarm_links(l)))

    async def patch(self):
        a_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l_row = await conn.fetchrow('SELECT acknowledged FROM alarms WHERE id = $1', a_id)
            if not l_row:
                raise web.HTTPNotFound
            body = await self._valid_json(self.request)
            alarm = alarm_patch_schema.load(body)
            if alarm['acknowledged']:
                await conn.execute('UPDATE alarms SET ack_ts = now() WHERE id = $1', a_id)
            else:
                await conn.execute('UPDATE alarms SET ack_ts = NULL WHERE id = $1', a_id)
        raise web.HTTPNoContent

    async def delete(self):
        a_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            a_row = await conn.fetchrow('SELECT id FROM alarms WHERE id = $1', a_id)
            if not a_row:
                raise web.HTTPNotFound
            await conn.execute('DELETE from alarms where id = $1', a_id)
        raise web.HTTPNoContent
