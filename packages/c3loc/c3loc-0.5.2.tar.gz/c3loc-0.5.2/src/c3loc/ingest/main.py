#!/bin/env python
"""Reference Implementation of v1 C3 Security Beacon Auth Server."""
import asyncio
import asyncpg
import os
import signal

import click

from .protocol import ListenerProtocol
from ..db import init_db_pool


def default_handler(loop, context):
    print(f"Unhandled exception: {context['message']}", context)
    loop.stop()


@click.command()
@click.option('--port', '-p', default=9999)
def main(port) -> None:
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(default_handler)
    if signal is not None and os.name != 'nt':
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    db_pool = loop.run_until_complete(init_db_pool())
    ListenerProtocol.db_pool = db_pool

    def start_server(loop):
        return loop.create_server(ListenerProtocol, '0.0.0.0', port)
    server = loop.run_until_complete(start_server(loop))
    print("Listening on port {}".format(port))
    loop.run_forever()
    server.close()
    loop.close()


if __name__ == '__main__':
    main()
