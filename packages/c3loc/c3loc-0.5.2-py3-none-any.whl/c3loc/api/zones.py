import json

from aiohttp import web

from .schemas import zones_schema, zone_schema
from .views import ValidatingView, paginate_query


class ZonesView(ValidatingView):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = ('SELECT * from zones', )
            tags = await conn.fetch(*paginate_query(self.request, query))
            return web.json_response(zones_schema.dump(tags))

    async def post(self):
        body = await self._valid_json(self.request)
        new_z = self._validate(zone_schema, body)

        if 'attrs' not in new_z:
            new_z['attrs'] = {}

        async with self.request.app['db_pool'].acquire() as conn:
            await conn.execute('INSERT INTO zones (name, attrs) VALUES ($1, $2)',
                         new_z['name'], json.dumps(new_z['attrs']))
        raise web.HTTPCreated


class ZoneView(ValidatingView):
    async def get(self):
        z_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l = await conn.fetchrow('SELECT * FROM zones WHERE id = $1', z_id)
            if not l:
                raise web.HTTPNotFound
            return web.json_response(zone_schema.dump(l))

    async def patch(self):
        z_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l_row = await conn.fetchrow('SELECT name, attrs FROM zones WHERE id = $1', z_id)
            if not l_row:
                raise web.HTTPNotFound
            zone = zone_schema.load(dict(l_row.items()))
            body = await self._valid_json(self.request)
            new = self._validate(zone_schema, body)
            zone.update(new)
            await conn.execute('UPDATE zones SET name = $1, attrs = $2 WHERE id = $3',
                               zone['name'], json.dumps(zone['attrs']), z_id)
        raise web.HTTPNoContent

    async def delete(self):
        z_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l_row = await conn.fetchrow('SELECT name, attrs FROM zones WHERE id = $1', z_id)
            if not l_row:
                raise web.HTTPNotFound
            await conn.execute('DELETE from zones where id = $1', z_id)
        raise web.HTTPNoContent
