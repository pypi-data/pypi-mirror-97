import asyncio

from typing import (
    Any, Iterable,
    Mapping,
    MutableMapping,
    List, Tuple,
    Set, Union,
)

from aiohttp import web
import aiohttp_cors
from aiotools import apartial

from .utils import check_api_params, call_non_bursty
from .typing import CORSOptions, WebMiddleware
from .wsproxy import TCPProxy


async def serve_deployment(request: web.Request) -> web.StreamResponse:
    registry = request.app['registry']
    deployment_id = request.match_info['deployment_id']
    access_key = request['keypair']['access_key']
    service = request.query.get('app', None)  # noqa

    'db-query kernels that belong to the deployment'
    'check permission, visibility, is_active'

    if 'kernel does not exist for the service':
        'create a new kernel for deployment'
    else:
        'use the kernel'
        # TODO: auto-scale?

    'check the query parameter and:'
    ' - start the appropriate service'
    ' - proxy binary traffic to the service'

    async def refresh_cb(kernel_id: str, data: bytes):
        await asyncio.shield(call_non_bursty(
            kernel_id,
            apartial(registry.refresh_session, sess_id, access_key),
            max_bursts=64, max_idle=2000))

    down_cb = apartial(refresh_cb, kernel.id)
    up_cb = apartial(refresh_cb, kernel.id)
    ping_cb = apartial(refresh_cb, kernel.id)

    result = await asyncio.shield(
        registry.start_service(sess_id, access_key, service, opts))
    if result['status'] == 'failed':
        msg = f"Failed to launch the app service: {result['error']}"
        raise InternalServerError(msg)

    ws = web.WebSocketResponse(autoping=False)
    await ws.prepare(request)
    proxy = TCPProxy(ws, dest[0], dest[1],
                     downstream_callback=down_cb,
                     upstream_callback=up_cb,
                     ping_callback=ping_cb)
    return await proxy.proxy()


async def init(app: web.Application) -> None:
    pass


async def shutdown(app: web.Application) -> None:
    pass


def create_app(default_cors_options: CORSOptions) -> Tuple[web.Application, Iterable[WebMiddleware]]:

    app = web.Application()
    app.on_startup.append(init)
    app.on_shutdown.append(shutdown)
    app['prefix'] = 'deployment'
    cors = aiohttp_cors.setup(app, defaults=default_cors_options)
    add_route = app.router.add_route
    cors.add(add_route('GET', r'/{deployment_id}', serve_deployment))
    return app, []
