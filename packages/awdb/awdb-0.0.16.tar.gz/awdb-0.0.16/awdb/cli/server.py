import asyncio
from aiohttp import web
from ..utils import Client
import logging
from inspect import isawaitable

_logger = logging.getLogger(__name__)


class DebuggerClient(Client):

    def __init__(self, websocket):
        super(DebuggerClient, self).__init__(websocket)
        self.subscribers = set()

    def subscribe(self, client):
        self.subscribers.add(client)

    def unsubscribe(self, client):
        self.subscribers.remove(client)

    async def on_read(self, dat):
        for client in self.subscribers:
            await client.send_queue.put(dat)


class DebuggingClient(Client):
    def __init__(self, websocket, servers):
        super(DebuggingClient, self).__init__(websocket)
        self.servers = servers
        self.auto_subscribe = False

    async def on_read(self, data):
        event_method = 'on_event_{}'.format(data.get('action'))

        if hasattr(self, event_method):
            result = getattr(self, event_method)(data)
            if isawaitable(result):
                await result

    async def on_event_call(self, data):
        for server in self.servers:
            if server.uuid == data.get('uuid'):
                await server.send_queue.put(data.get('params'))

    def on_event_subscribe(self, data):
        for server in self.servers:
            if server.uuid == data.get('uuid'):
                server.subscribe(self)

    def on_event_unsubscribe(self, data):
        for server in self.servers:
            if server.uuid == data.get('uuid'):
                server.unsubscribe(self)

    def on_event_add_user(self, data):
        username = data.get('username')
        if username not in users:
            users[username] = set()

    def on_event_rm_user(self, data):
        username = data.get('username')
        if username in users:
            del users[username]

    def on_event_autosubscribe(self, data):
        self.auto_subscribe = data.get('params', [False])[0]

    async def on_event_kill(self, data):
        to_remove = set()

        for server in self.servers:
            if server.uuid == data.get('uuid'):
                to_remove.add(server)

        for server in to_remove:
            self.servers.remove(server)
            try:
                await server.close()
            except Exception:
                pass

    async def on_event_list(self, data):
        await self.send_queue.put({
            "type": "instances",
            "instances": [
                {
                    "uuid": server.uuid,
                    "tags": server.tags
                }
                for server in
                self.servers
            ]
        })


debugging_sessions = set()
debugging_clients = set()
users = dict()


async def start_aiohttp():
    import os

    logging.basicConfig(level='DEBUG')

    _logger.info("Starting server")

    async def websocket_handler(request):
        _logger.info("New Request")
        done = False
        client = None
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        _logger.info("New connexion")

        data = await ws.receive_json()
        print(data)

        if data.get('event') == 'new_session':
            _logger.info("Got new debug")
            client = DebuggerClient(ws)
            client.uuid = data.get('uuid')
            client.tags = data.get('tags', [])
            debugging_sessions.add(client)

            for sb_client in debugging_clients:
                if sb_client.auto_subscribe:
                    client.subscribe(sb_client)

        elif data.get('event') == 'new_client':
            _logger.info("Got new client")
            data = await ws.receive_json()

            if data.get('action') == 'authenticate':
                if data.get('token') not in users:
                    done = True
                else:
                    client = DebuggingClient(ws, debugging_sessions)
                    client.uuid = data.get('client_id')
                    client.token = data.get('token')
                    client.user_info = data.get('client_info')

                    users[client.token].add(client)
                    debugging_clients.add(client)
            else:
                done = True

        while not done:
            await client.event_loop()
            try:
                if client.stopped:
                    await client.stop()
                    break
            except KeyboardInterrupt:
                await client.on_read(None)

        if isinstance(client, DebuggerClient):
            debugging_sessions.remove(client)
        elif isinstance(client, DebuggingClient):
            debugging_clients.remove(client)
            users[client.token].remove(client)

        _logger.info('websocket connection closed')

        return ws

    if os.environ.get('AWDB_ADMIN_TOKEN'):
        users[os.environ.get('AWDB_ADMIN_TOKEN')] = set()

    app = web.Application()
    bind_host = os.environ.get('AWDB_BIND_HOST', 'localhost')
    bind_port = int(os.environ.get('AWDB_BIND_PORT', '8080'))
    app.add_routes([web.get('/ws', websocket_handler)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, bind_host, bind_port)
    _logger.info("Serving on http://{}:{}".format(bind_host, bind_port))
    await site.start()

    while True:
        try:
            await asyncio.sleep(3600)
        except KeyboardInterrupt:
            break

    await runner.cleanup()


def server():
    logging.basicConfig(level='INFO')
    loop = asyncio.get_event_loop()
    app = start_aiohttp()
    loop.run_until_complete(app)
