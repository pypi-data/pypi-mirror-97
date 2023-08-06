#!/bin/env python
"""Reference Implementation of v1 C3 Security Beacon Auth Server."""
from aiohttp import web
import aiohttp_cors
import asyncio
from functools import partial
import os
import signal

import click

from ..db import init_db_pool
from .alarms import AlarmsView, AlarmView
from .listeners import ListenersView, ListenerView
from .proximity import ProximityView, proximity_task
from .tags import TagsView, TagView, TagHistoryView
from .zones import ZonesView, ZoneView
from .groups import GroupsView, GroupView
from ..demo_fe.main import app as demo_fe_app


def default_handler(loop, context):
    print(f"Unhandled exception: {context['message']}", context)
    loop.stop()


@click.command()
@click.option('--port', '-p', default=5000)
@click.option('--demo-fe', is_flag=True, default=True)
def main(port, demo_fe) -> None:
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(default_handler)
    if signal is not None and os.name != 'nt':
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    async def init_db_app(app):
        app['db_pool'] = await init_db_pool()
        asyncio.ensure_future(proximity_task(app['db_pool']))

    app = web.Application()
    app.on_startup.append(init_db_app)
    app.router.add_view('/api/listeners', ListenersView)
    app.router.add_view('/api/listeners/{id:\w+}', ListenerView, name='listener')
    app.router.add_view('/api/zones', ZonesView)
    app.router.add_view('/api/zones/{id:\d+}', ZoneView, name='zone')
    app.router.add_view('/api/tags', TagsView)
    app.router.add_view('/api/tags/{id:\d+}', TagView, name='tag')
    app.router.add_view('/api/tags/{id:\d+}/history', TagHistoryView, name='history')
    app.router.add_view('/api/proximity', ProximityView)
    app.router.add_view('/api/groups', GroupsView)
    app.router.add_view('/api/groups/{id:\d+}', GroupView, name='group')
    app.router.add_view('/api/alarms', AlarmsView)
    app.router.add_view('/api/alarms/{id:\d+}', AlarmView, name='alarm')

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    if demo_fe:
        app.add_subapp('/demo', demo_fe_app)
    web.run_app(app, port=port)


if __name__ == '__main__':
    main()
