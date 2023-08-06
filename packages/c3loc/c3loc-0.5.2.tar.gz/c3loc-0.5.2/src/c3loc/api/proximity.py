from aiohttp import web
from aiohttp_cors import CorsViewMixin
import asyncpg
import asyncio

from .schemas import prox_schema
from .views import paginate_query
from ..config import CONFIG

THE_QUERY = \
"""
SELECT tags.distance,
       zones.name as zone_name,
       tags.name as tag_name,
       tags.type as tag_type,
       last_seen,
       tags.id as tag_id,
       zone_id,
       alarm_active
FROM tags
LEFT JOIN zones on zones.id = zone_id
ORDER BY tags.id DESC
"""

THE_TYPE_QUERY = \
"""
SELECT tags.distance,
       zones.name as zone_name,
       tags.name as tag_name,
       tags.type as tag_type,
       last_seen,
       tags.id as tag_id,
       zone_id,
       alarm_active
FROM tags
LEFT JOIN zones on zones.id = zone_id
WHERE tags.type = $1
ORDER BY tags.id DESC
"""

THE_GROUP_QUERY = \
"""
SELECT tags.distance,
       zones.name as zone_name,
       tags.name as tag_name,
       tags.type as tag_type,
       last_seen,
       tags.id as tag_id,
       zone_id,
       alarm_active
FROM tags
LEFT JOIN zones on zones.id = zone_id
WHERE tags.group_id = $1
ORDER BY tags.id DESC
"""
# """SELECT zones.name as zone_name, tags.name as tag_name, a.*
# FROM (SELECT log.tag_id, zone_id, anchor_dist as distance, log.ts, anchor_id from log
#     JOIN (SELECT tag_id, max(ts) max_ts from log WHERE anchor_id IS NOT NULL GROUP BY tag_id) temp
#         ON log.tag_id = temp.tag_id AND log.ts = temp.max_ts
# UNION SELECT DISTINCT ON (log.tag_id) log.tag_id, zone_id, distance_cm as distance, log.ts, anchor_id from log
#     JOIN (SELECT tag_id, min(distance_cm), ts from log
#           WHERE anchor_id IS NULL and ts > ((now() at time zone 'utc') - interval '1 min') GROUP BY tag_id, ts ORDER BY ts DESC) temp
#     ON log.tag_id = temp.tag_id AND log.ts = temp.ts) a
# LEFT JOIN zones on zone_id = zones.id
# LEFT JOIN tags on tag_id = tags.id"""


def process_prox_results(results):
    output = []
    for r in results:
        zone_id = r['zone_id']
        d_r = dict(r)
        d_r['links'] = {
            "zone": f"/api/zones/{zone_id}" if zone_id else None,
            "tag": f"/api/tags/{r['tag_id']}"
        }
        output.append(d_r)
    return output


class ProximityView(web.View, CorsViewMixin):
    async def get(self):
        if 'type' in self.request.query:
            t = self.request.query['type']
            query = (THE_TYPE_QUERY, t)
        elif 'group_id' in self.request.query:
            g = self.request.query['group_id']
            try:
                query = (THE_GROUP_QUERY, int(g))
            except ValueError:
                raise web.HTTPBadRequest(text='Invalid group id')
        else:
            query = (THE_QUERY,)
        query = paginate_query(self.request, query)
        async with self.request.app['db_pool'].acquire() as conn:
            try:
                results = await conn.fetch(*query)
            except asyncpg.exceptions.InvalidTextRepresentationError:
                raise web.HTTPBadRequest(text='Bad tag type in query')
            return web.json_response(prox_schema.dump(process_prox_results(results)))


async def proximity_task(pool):
    query = """UPDATE tags SET zone_id = cf.zone_id, distance = cf.distance FROM
(SELECT DISTINCT ON (upper.tag_id)
    coalesce(anchor_dist, upper.distance) as distance,
    upper.tag_id, tags.zone_id from log upper
LEFT JOIN tags on tags.id = upper.anchor_id
WHERE ts > tags.last_seen - interval '10s'
ORDER BY upper.tag_id, distance, upper.ts DESC) as cf
WHERE tags.id = cf.tag_id;
"""
    period = CONFIG['LOCATION_UPDATE_MS'] / 1000
    count = 0

    while True:
        async with pool.acquire() as conn:
            await conn.execute(query)
            count += 1
            if count % 60 == 0:  # Once per minute
                await conn.execute("DELETE FROM log WHERE ts < current_timestamp - interval '5m'")
            await asyncio.sleep(period)
