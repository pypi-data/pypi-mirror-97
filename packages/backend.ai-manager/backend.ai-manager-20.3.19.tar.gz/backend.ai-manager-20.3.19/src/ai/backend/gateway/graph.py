'''
Task graph APIs to execute a graph of tasks from task templates.
'''

from typing import (
    Tuple,
    Iterable,
)

from aiohttp import web
import aiohttp_cors

from .auth import auth_required
from .manager import ALL_ALLOWED, READ_ALLOWED, server_status_required
from .typing import CORSOptions, WebMiddleware


@server_status_required(ALL_ALLOWED)
@auth_required
async def create(request: web.Request) -> web.Response:
    raise NotImplementedError


@server_status_required(READ_ALLOWED)
@auth_required
async def get_info(request: web.Request) -> web.Response:
    raise NotImplementedError


@server_status_required(READ_ALLOWED)
@auth_required
async def get_tasks(request: web.Request) -> web.Response:
    raise NotImplementedError


@server_status_required(ALL_ALLOWED)
@auth_required
async def destroy(request: web.Request) -> web.Response:
    raise NotImplementedError


@server_status_required(ALL_ALLOWED)
@auth_required
async def execute(request: web.Request) -> web.Response:
    raise NotImplementedError


async def init(app: web.Application) -> None:
    pass


async def shutdown(app: web.Application) -> None:
    pass


def create_app(default_cors_options: CORSOptions) -> Tuple[web.Application, Iterable[WebMiddleware]]:
    app = web.Application()
    app.on_startup.append(init)
    app.on_shutdown.append(shutdown)
    app['api_versions'] = (4,)
    # cors = aiohttp_cors.setup(app, defaults=default_cors_options)
    # cors.add(app.router.add_route('POST', '', create))
    # kernel_resource = cors.add(app.router.add_resource(r'/{graph_id}'))
    # cors.add(kernel_resource.add_route('GET',    get_info))
    # # cors.add(kernel_resource.add_route('GET',    get_tasks))
    # cors.add(kernel_resource.add_route('DELETE', destroy))
    # cors.add(kernel_resource.add_route('POST',   execute))
    return app, []
