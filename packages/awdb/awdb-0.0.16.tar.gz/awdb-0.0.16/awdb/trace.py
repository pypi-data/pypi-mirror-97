import inspect
import sys
from .utils import Client
from .exceptions import StopDebugger
from .serializer import Serializer
import threading
from threading import Thread
import asyncio
import atexit
import time
import uuid
import os
import ctypes
import logging
import aiohttp
from functools import lru_cache
from concurrent.futures import TimeoutError

if hasattr(asyncio.Task, 'all_tasks'):
    all_tasks = asyncio.Task.all_tasks
else:
    all_tasks = asyncio.all_tasks

debugger = threading.local()
debugger.instance = None

_logger = logging.getLogger(__name__)


#    def safe_serialize_dict(obj):
#        res = {}
#        for key, value in obj.items():
#            if isinstance(value, (str, int, float, )):
#                res[key] = value
#            else:
#                try:
#                    res[key] = repr(value)
#                except Exception:
#                    res[key] = "Couldn't convert to string"
#        return res
# 
# 
#    def safe_serialize_tuple(obj):
#        if isinstance(obj, tuple):
#            return [
#                repr(val)
#                for val in obj
#            ]
#        else:
#            return repr(obj)

serializer = Serializer()

class DbClient(Client):
    def __init__(self, websocket, debugger):
        super(DbClient, self).__init__(websocket)
        self.debugger = debugger
        debugger.client_obj = self
        self.break_files = []

    async def on_read(self, data):
        if (
            data.get("action") == "configure" and
            data.get('type') == 'break'
        ):
            self.break_files = data.get('files')
            return

        if (
            data.get("action") == "interrupt"
        ):
            self.debugger.mode = 'step'

        if (
            data.get("action") == "stop"
        ):
            await self.stop()

        await super(DbClient, self).on_read(data)

    async def on_write(self, data):
        pass

    # async def event_loop(self):
    #     if self.debugger.stopped:
    #         self.on_exit()
    #         return
    #     await super(Client, self).event_loop()


class FakeDebugger(object):
    def __init__(self):
        self.stopped = True

    def stop(self):
        pass


def client_thread(parent_debugger):
    try:
        if debugger.instance:
            debugger.instance.stopped = True
    except Exception:
        debugger.instance = FakeDebugger()

    def get_tags():
        env = os.environ.copy()
        tags = []
        for key, value in env.items():
            if key.startswith('AWDB_TAGS_'):
                tags += [
                    val.strip()
                    for val in value.split(',')
                ]

        tags.append("thread:{}".format(threading.current_thread().getName()))

        return tags

    async def connect():
        try:
            HOSTNAME = os.environ.get('AWDB_URL', 'wss://awdb.docker/ws')
            VERIFY_SSL = os.environ.get('AWDB_VERIFY_SSL', 'TRUE')
            verify_ssl = VERIFY_SSL == "TRUE"
            connector = aiohttp.TCPConnector(verify_ssl=verify_ssl)
            session = aiohttp.ClientSession(connector=connector)
            websocket = await session.ws_connect(HOSTNAME)

            client = DbClient(websocket, parent_debugger)
            client.loop = asyncio.get_event_loop()
            client.uuid = uuid.uuid1()

            init_session = {
                "event": "new_session",
                "uuid": client.uuid.hex,
                "tags": get_tags()
            }

            await websocket.send_json(init_session)

            while True:
                if parent_debugger.stopped:
                    await client.stop()
                    return

                await client.event_loop()

            _logger.debug("Ended client")
            await session.close()
        except Exception:
            _logger.info("Exception occured exiting task cleanly")

    try:
        loop = asyncio.new_event_loop()
        task = asyncio.ensure_future(connect(), loop=loop)
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass

    tasks = all_tasks(loop)
    for task in tasks:
        try:
            task.cancel()
        except Exception:
            pass

    parent_debugger.stopped = True


class DebuggingContext(object):
    def __init__(self, frame, event, arg):
        self.frame = frame
        self.event = event
        self.arg = arg
        self.frame_stack = []

    def push_frame(self):
        if self.frame.f_back:
            self.frame_stack.append(self.frame)
            self.frame = self.frame.f_back

    def pop_frame(self):
        if len(self.frame_stack) > 0:
            self.frame = self.frame_stack.pop()


@lru_cache(256)
def compile_code(code, name, mode):
    return compile(code, name, mode)


def refresh_frame(frame):
    ctypes.pythonapi.PyFrame_LocalsToFast(
        ctypes.py_object(frame),
        ctypes.c_int(0)
    )


def eval_code(context, params):
    text_code = params.get('code')
    try:
        code = compile_code(text_code, '<eval>', 'eval')
        ret_val = eval(
            code,
            context.frame.f_globals,
            context.frame.f_locals,
        )
    except Exception:
        local_values = context.frame.f_locals.copy()
        try:
            code = compile_code(text_code, '<exec>', 'exec')
            ret_val = eval(
                code,
                context.frame.f_globals,
                local_values
            )
            context.frame.f_locals.update(local_values)
            refresh_frame(context.frame)
        except Exception:
            _logger.error("Got error", exc_info=True)
            ret_val = None
    return ret_val


def set_locals(context, params):
    context.frame.f_locals.update({
        params.get('key'): params.get('value')
    })
    refresh_frame(context.frame)


class Debugger(object):
    def __init__(self):
        self.client = Thread(target=client_thread, args=(self,), daemon=True)
        self.client.start()
        self.client_obj = None
        self.stopped = False

        self.thread_name = threading.current_thread().getName()
        self.breakpoints = []
        self.mode = 'step'
        self.break_on_return = False
        self.return_frame = None

        while not self.client_obj and not self.stopped:
            _logger.debug(
                "[%s] Waiting for the client from the async thread ",
                self.thread_name
            )
            time.sleep(1)

    def test_breakpoints(self, frame, event):
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno

        for params in self.breakpoints:
            if len(params) == 3:
                b_event, b_lineno, b_filename = params
                condition = None
            else:
                b_event, b_lineno, b_filename, condition = params

            event_match = b_event == event or b_event == 'any'
            if not event_match:
                continue

            filename_match = b_filename == filename or b_filename == 'any'
            if not filename_match:
                continue

            if b_lineno == 'any':
                lineno_match = True
            else:
                if isinstance(b_lineno, (tuple, list)):
                    lineno_match = b_lineno[0] <= lineno <= b_lineno[1]
                else:
                    lineno_match = b_lineno == lineno

            if not lineno_match:
                continue

            if condition:
                try:
                    return eval(
                        condition,
                        frame.f_globals.copy(),
                        frame.f_locals.copy()
                    )
                except Exception:
                    pass
            else:
                return True

    def should_break(self, frame, event, arg):
        if (
            self.break_on_return and
            event == 'return' and
            frame == self.return_frame
        ):
            self.break_on_return = False
            return True

        if self.test_breakpoints(frame, event):
            return True

        if self.mode == 'step':
            return True

        return False

    def inspect_frame(self, frame, event, arg):
        source_code, source_line = inspect.getsourcelines(frame.f_code)
        source = "".join(source_code)

        frame_locals = serializer.serialize(frame.f_locals)
        frame_globals = serializer.serialize(frame.f_globals)

        data = {
            "type": "frame",
            "session": self.client_obj.uuid.hex,
            "event": event,
            "arg": serializer.serialize(arg),
            "source": source,
            "source_lineno": source_line,
            "lineno": frame.f_lineno,
            "filename": frame.f_code.co_filename,
            "locals": frame_locals,
            "globals": frame_globals
        }

        return data

    def __call__(self, frame, event, arg):
        if self.stopped or not self.client_obj:
            return

        if not self.should_break(frame, event, arg):
            return self

        thread_name = threading.current_thread().getName()
        _logger.debug(
            "Start Trace (%s) %s %s",
            thread_name,
            event,
            arg
        )

        context = DebuggingContext(frame, event, arg)

        data = self.inspect_frame(frame, event, arg)
        self.send_queue(data)

        # frame_stack = []
        # current_frame = frame
        while True:
            obj = self.receive_queue()

            if isinstance(obj, StopDebugger):
                return self

            if obj['action'] in ['step', 's']:
                self.mode = 'step'
                return self
            if obj['action'] in ['return', 'r']:
                self.break_on_return = True
                self.return_frame = frame
                self.mode = 'continue'
                return self
            elif obj['action'] == 'stop':
                _logger.debug("[%s] Removing trace to continue", thread_name)
                self.mode = 'step'
                sys.settrace(None)
                return
            elif obj['action'] in ['continue', 'c']:
                _logger.debug("[%s] Removing trace to continue", thread_name)
                self.mode = 'continue'
                return self
            elif obj.get('action') == 'set_locals':
                set_locals(context, obj)
            elif obj.get('action') == 'execute':
                ret_val = eval_code(context, obj)
                self.send_queue({
                    "type": "retval",
                    "value": repr(ret_val)
                })
            elif obj.get('action') == 'add_breakpoint':
                _logger.debug("Adding breakpoint")
                breakpt = obj.get('breakpoint')
                try:
                    if breakpt and len(breakpt) == 4:
                        breakpt = breakpt[:-1] + [
                            compile_code(breakpt[-1], 'breakpoint', 'eval')
                        ]
                    self.breakpoints.append(breakpt)
                except Exception:
                    pass
            elif obj.get('action') == 'remove_breakpoint':
                self.breakpoints.remove(obj.get('breakpoint'))
            elif obj.get('action') == 'breakpoints':
                self.send_queue({
                    "type": "breakpoints",
                    "breakpoints": [
                        [bp[0], bp[1], bp[2]]
                        for bp in self.breakpoints
                    ]
                })
            elif obj.get('action') == 'inspect':
                data = self.inspect_frame(context.frame, event, arg)
                self.send_queue(data)
            elif obj.get('action') == 'up':
                context.push_frame()
                data = self.inspect_frame(
                    context.frame,
                    context.event,
                    context.arg
                )
                self.send_queue(data)
            elif obj.get('action') == 'down':
                context.pop_frame()
                data = self.inspect_frame(
                    context.frame,
                    context.event,
                    context.arg
                )
                self.send_queue(data)
            elif obj.get('action') == 'w':
                action = self.get_call_stack(context.frame)
                self.send_queue(action)
            else:
                _logger.info(
                    "Unknown command waiting for next command"
                )

            self.send_queue({'action': 'none'})

        return self

    def get_call_stack(self, frame):
        frames = inspect.getouterframes(frame)

        frames.reverse()

        return {
            "type": "frames",
            "frames": [
                {
                    "filename": info.filename,
                    "lineno": info.lineno,
                    "function": info.function
                }
                for info in frames
            ]
        }

    def send_queue(self, data):
        queue = self.client_obj.send_queue

        async def put_queue(data):
            sleep_task = asyncio.ensure_future(asyncio.sleep(1))
            put_task = asyncio.ensure_future(queue.put(data))
            attempts = 0

            while True:
                _logger.debug("Put data into queue {}".format(attempts))
                done, pending = await asyncio.wait(
                    [sleep_task, put_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                if put_task in done:
                    return await put_task
                else:
                    await sleep_task

                # Allow unblocking the thread in case it's stopped
                if self.client_obj.stopped:
                    return StopDebugger()

                sleep_task = asyncio.ensure_future(asyncio.sleep(1))
                attempts += 1

        loop = self.client_obj.loop
        result = asyncio.run_coroutine_threadsafe(put_queue(data), loop)
        while True:
            try:
                if self.stopped:
                    return StopDebugger()
                else:
                    return result.result(timeout=1)
            except TimeoutError:
                pass

    def receive_queue(self):
        async def get_queue():
            sleep_task = asyncio.ensure_future(asyncio.sleep(1))
            get_task = asyncio.ensure_future(self.client_obj.recv_queue.get())
            attempts = 0

            while True:
                _logger.debug("Getting data from queue {}".format(attempts))

                done, pending = await asyncio.wait(
                    [sleep_task, get_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                if get_task in done:
                    return await get_task
                else:
                    await sleep_task

                # Allow unblocking the thread in case it's stopped
                if self.client_obj.stopped:
                    return StopDebugger()

                sleep_task = asyncio.ensure_future(asyncio.sleep(1))
                attempts += 1

        async def run_task():
            return await task

        loop = self.client_obj.loop
        task = asyncio.ensure_future(get_queue(), loop=loop)
        result = asyncio.run_coroutine_threadsafe(run_task(), loop)
        while True:
            try:
                if self.stopped:
                    return StopDebugger()
                else:
                    return result.result(timeout=1)
            except TimeoutError:
                pass

    def stop(self):
        self.stopped = True

        if sys.gettrace() == self:
            sys.settrace(None)

        if self.client_obj:
            self.client_obj.stopped = True

        self.client.join()


def set_trace():
    _logger.debug("[%s] Set trace", threading.current_thread().getName())
    thread_name = threading.current_thread().getName()

    try:
        instance = debugger.instance
        if not instance or instance.stopped:
            debugger.instance = Debugger()
            instance = debugger.instance
    except Exception:
        debugger.instance = Debugger()
        instance = debugger.instance

    def destroy(instance):
        def wrap():
            _logger.debug("[%s] Destroying debugger instance", thread_name)
            instance.stop()
        return wrap

    atexit.register(destroy(instance))

    frame = sys._getframe().f_back
    while frame:
        frame.f_trace = instance
        frame = frame.f_back

    if not instance.stopped:
        instance.mode = 'step'
        _logger.debug("[%s] Set trace to %s", thread_name, instance)
        sys.settrace(instance)
    else:
        _logger.debug("[%s] Remove trace", thread_name)
        sys.settrace(None)
