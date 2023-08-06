import json

from aiohttp import web

from .schemas import groups_schema, group_schema
from .views import ValidatingView, paginate_query


class GroupsView(ValidatingView):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = ('SELECT * from groups', )
            tags = await conn.fetch(*paginate_query(self.request, query))
            return web.json_response(groups_schema.dump(tags))

    async def post(self):
        body = await self._valid_json(self.request)
        new_z = self._validate(group_schema, body)

        if 'attrs' not in new_z:
            new_z['attrs'] = {}

        async with self.request.app['db_pool'].acquire() as conn:
            await conn.execute('INSERT INTO groups (name, attrs) VALUES ($1, $2)',
                         new_z['name'], json.dumps(new_z['attrs']))
        raise web.HTTPCreated


class GroupView(ValidatingView):
    async def get(self):
        z_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l = await conn.fetchrow('SELECT * FROM groups WHERE id = $1', z_id)
            if not l:
                raise web.HTTPNotFound
            return web.json_response(group_schema.dump(l))

    async def patch(self):
        z_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l_row = await conn.fetchrow('SELECT name, attrs FROM groups WHERE id = $1', z_id)
            if not l_row:
                raise web.HTTPNotFound
            group = group_schema.load(dict(l_row.items()))
            body = await self._valid_json(self.request)
            new = self._validate(group_schema, body)
            group.update(new)
            await conn.execute('UPDATE groups SET name = $1, attrs = $2 WHERE id = $3',
                               group['name'], json.dumps(group['attrs']), z_id)
        raise web.HTTPNoContent

    async def delete(self):
        z_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l_row = await conn.fetchrow('SELECT name, attrs FROM groups WHERE id = $1', z_id)
            if not l_row:
                raise web.HTTPNotFound
            await conn.execute('DELETE from groups where id = $1', z_id)
        raise web.HTTPNoContent
