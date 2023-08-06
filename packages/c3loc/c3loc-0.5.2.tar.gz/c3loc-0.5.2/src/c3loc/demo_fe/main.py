#!/bin/env python

import pkg_resources
from aiohttp import web
import aiohttp_jinja2
import jinja2


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('c3loc', 'templates'))

@aiohttp_jinja2.template('index.html')
async def prox(request):
    return {}


@aiohttp_jinja2.template('tag_form.html')
async def tag_get(request):
    return {'tag_id': request.match_info['id']}


@aiohttp_jinja2.template('zone_form.html')
async def zone_get(request):
    return {'zone_id': request.match_info['id']}


@aiohttp_jinja2.template('add_zone.html')
async def add_zone(request):
    pass


app.router.add_static('/static/',
                      path=pkg_resources.resource_filename('c3loc', 'static'),
                      name='static')
app.router.add_get('/', prox)
app.router.add_get('/tags/{id:\d+}', tag_get)
app.router.add_get('/zones/{id:\d+}', zone_get)
app.router.add_get('/zones', add_zone)
