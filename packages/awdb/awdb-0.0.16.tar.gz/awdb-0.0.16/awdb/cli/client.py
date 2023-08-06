import ast
import json
import logging
import os
import tempfile
from subprocess import call

_logger = logging.getLogger(__name__)

logging.basicConfig(level='INFO')


class JSON(object):
    def __init__(self, data):
        self.data = data

    def __format__(self, format):
        return json.dumps(self.data, indent=2, sort_keys=True)


frame_template = """
{session}
{event}
{filename}:{lineno}:{source_lineno}
{arg_json}

Locals:
{locals_json}

Globals:
{globals_json}

Code:
{source}
"""

def parse_line_num(line):
    if ':' in line:
        lines = line.split(':')
        line = [
            int(lines[0]),
            int(lines[1])
        ]
    elif line != 'any':
        line = int(line)

    return line


def parse_break_line(command):
    _, rest = command.split(' ', 1)
    event, rest = rest.split(' ', 1)
    line = None

    rest = rest.split(' ', 1)

    if ':' in rest[0]:
        filename, line = rest[0].split(':', 1)
        line = parse_line_num(line)
    else:
        filename = rest[0]

    if len(rest) == 1:
        return [event, line, filename]

    rest = rest[1]

    rest = rest.split(' ', 1)

    if len(rest) == 1:
        line = rest[0]
        cond = False
    else:
        line = rest[0]
        cond = rest[1]

    line = parse_line_num(line)

    if cond:
        return [event, line, filename, cond]
    else:
        return [event, line, filename]


def parse_command(command):
    if command in [
        'step',
        's',
        'continue',
        'c',
        'stop',
        'inspect',
        'return',
        'interrupt',
        'breakpoints',
        'w',
        'up',
        'down',
    ]:
        return {'action': command}
    elif command.startswith('set'):
        _, vals = command.split(' ', 1)
        key, value = command.split(' ')
        action = {
            'action': 'set_locals',
            'key': key,
            'value': ast.literal_eval(value)
        }
        return action
    elif command.startswith('eval+'):
        editor = os.environ.get('editor', 'vim')
        with tempfile.NamedTemporaryFile(suffix='.py') as fin:
            call([editor, fin.name])
            fin.seek(0)
            code = fin.read().decode('utf-8')
        print(code)
        action = {
            'action': 'execute',
            'code': code
        }
        return action
    elif command.startswith('eval'):
        _, code = command.split(' ', 1)
        action = {
            'action': 'execute',
            'code': code
        }
        return action
    elif command.startswith('break'):
        action = {
            "action": "add_breakpoint",
            "breakpoint": parse_break_line(command)
        }
        return action
    elif command.startswith('-break'):
        action = {
            "action": "remove_breakpoint",
            "breakpoint": parse_break_line(command)
        }
        return action
    else:
        action = {
            'action': 'execute',
            'code': command
        }
        return action


async def format_response(data):
    from aioconsole import aprint
    if data.get('type') == 'frame':
        lineno = data.get('lineno', 0) - data.get('source_lineno', 0)

        source = "\n".join([
            "{}{}".format(
                '->' if index == lineno else '  ',
                line
            )
            for index, line in enumerate(data.get('source').split('\n'))
        ])

        data['source'] = source

        data.update({
            "locals_json": JSON(data['locals']),
            "globals_json": JSON(data['globals']),
            "arg_json": JSON(data['arg']),
        })

        await aprint(frame_template.format(**data))
    elif data.get('type') == 'frames':
        await aprint("Call stack")
        for info in data.get('frames', []):
            await aprint(
                " {filename}:{lineno} in {function}".format(**info)
            )
    elif data.get('type') == 'instances':
        await aprint("Instances")
        for instance in data.get('instances', []):
            await aprint("{uuid}: {tags}".format(**instance))
    elif data.get('type') == 'breakpoints':
        await aprint("Breakpoints")
        for parts in data.get('breakpoints', []):
            event = parts[0]
            filename = parts[2]
            line = parts[1]

            if len(parts) == 3:
                print("Event: {} File: {}:{}".format(event, filename, line))
            else:
                print("Event: {} File: {}:{}\n".format(event, filename, line, parts[3]))

    elif data.get('type') == 'retval':
        await aprint(data.get('value'))


def client():
    import aiohttp
    import asyncio
    import os
    from aioconsole import aprint

    HOSTNAME = os.environ.get('AWDB_URL', 'wss://awdb.docker/ws')
    print(HOSTNAME)

    async def get_command(active):
        from aioconsole import ainput
        prompt = "({})".format(active) if active else ""
        return await ainput("command {}> ".format(prompt))

    async def prompt(prompt):
        from aioconsole import ainput
        return await ainput("{}> ".format(prompt))

    async def execute_commands():
        connector = aiohttp.TCPConnector(verify_ssl=False)
        session = aiohttp.ClientSession(connector=connector)
        websocket = await session.ws_connect(HOSTNAME)

        active = None
        read = None

        await websocket.send_json({
            "event": "new_client"
        })

        token = os.environ.get('AWDB_TOKEN')
        if not token:
            token = await prompt("Token")

        username = os.environ.get('AWDB_USERNAME')
        if not username:
            username = await prompt("Username")

        await websocket.send_json({
            "action": "authenticate",
            "token": token,
            "client_id": 1,
            "client_info": {
                "username": username,
            }
        })

        while True:
            input_task = asyncio.ensure_future(get_command(active))
            if not read:
                read = asyncio.ensure_future(websocket.receive_json())

            done, pending = await asyncio.wait(
                [input_task, read],
                return_when=asyncio.FIRST_COMPLETED
            )

            if read in done:
                response = await read
                await format_response(response)
                read = None

            if input_task not in done:
                input_task.cancel()
                continue

            command = await input_task

            # prompt = "({})".format(active) if active else ""
            # command = input("command {}> ".format(prompt))

            action = None
            if not command:
                continue
                # if read:
                #     read.cancel()
                # break

            if command == 'list':
                action = {
                    'action': 'list'
                }
            elif command.startswith('auto'):
                action = {
                    'action': 'autosubscribe',
                    'params': [True]
                }
            elif command.startswith('use'):
                params = command.split(' ', 1)
                if len(params) == 2:
                    active = params[1]
            elif command.startswith('subscribe'):
                params = command.split(' ', 1)
                if len(params) == 2:
                    active = params[1]
                    action = {
                        'action': 'subscribe',
                        'uuid': active
                    }
            elif command.startswith('unsubscribe'):
                if active:
                    action = {
                        'action': 'unsubscribe',
                        'uuid': active
                    }
            elif command.startswith('add_user'):
                params = command.split(' ', 1)
                if len(params) == 2:
                    user = params[1]
                    action = {
                        'action': 'add_user',
                        'username': user
                    }
            elif command.startswith('rm_user'):
                params = command.split(' ', 1)
                if len(params) == 2:
                    user = params[1]
                    action = {
                        'action': 'rm_user',
                        'username': user
                    }
            elif command.startswith('kill'):
                action = {
                    'action': 'kill',
                    'uuid': active,
                }
                active = None
            else:
                action = parse_command(command)
                if action:
                    action = {
                        'action': 'call',
                        'params': action,
                        'uuid': active
                    }

            if action:
                await websocket.send_json(action)

                # while True:
                #     read = asyncio.create_task(websocket.receive_json())
                #     done, pending = await asyncio.wait({read}, timeout=1)
                #     if len(done) > 0:
                #         for dd in done:
                #             response = await dd
                #             format_response(response)
                #     else:
                #         read.cancel()
                #         break

        await websocket.close()
        await session.close()

        await aprint("done")

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(execute_commands())
    loop.run_until_complete(task)
