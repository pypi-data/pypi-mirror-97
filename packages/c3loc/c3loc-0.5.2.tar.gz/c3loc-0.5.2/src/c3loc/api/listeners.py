import json

from aiohttp import web
from asyncpg.exceptions import ForeignKeyViolationError

from marshmallow import ValidationError

from .schemas import listeners_schema, listener_schema
from .views import ValidatingView, paginate_query


class ListenersView(ValidatingView):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = ('SELECT * from listeners', )
            tags = await conn.fetch(*paginate_query(self.request, query))
            return web.json_response(listeners_schema.dump(tags))


class ListenerView(ValidatingView):
    async def get(self):
        l_id = self.request.match_info['id']
        async with self.request.app['db_pool'].acquire() as conn:
            l = await conn.fetchrow('SELECT * FROM listeners WHERE id = $1', l_id)
            if not l:
                raise web.HTTPNotFound
            return web.json_response(listener_schema.dump(l))

    async def patch(self):
        l_id = self.request.match_info['id']
        async with self.request.app['db_pool'].acquire() as conn:
            l_row = await conn.fetchrow('SELECT name, zone_id, attrs FROM listeners WHERE id = $1', l_id)
            if not l_row:
                raise web.HTTPNotFound
            from_db = listener_schema.load(dict(l_row.items()))
            body = await self._valid_json(self.request)
            new = self._validate(listener_schema, body)
            from_db.update(new)
            try:
                await conn.execute('UPDATE listeners SET name = $1, zone_id = $2, attrs = $3 WHERE id = $4',
                                   from_db['name'], from_db['zone_id'], json.dumps(from_db['attrs']), l_id)
            except ForeignKeyViolationError as e:
                raise web.HTTPBadRequest(reason=f'Invalid zone_id = {from_db["zone_id"]}')
        raise web.HTTPNoContent
