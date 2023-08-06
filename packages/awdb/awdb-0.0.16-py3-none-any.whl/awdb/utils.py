# -*- coding: utf-8 -*-
import asyncio
# import janus
import json
import logging

_logger = logging.getLogger(__name__)


class Read(object):
    def __init__(self, value):
        self.value = value


class Write(object):
    def __init__(self, value):
        self.value = value


class Client(object):
    def __init__(self, socket):
        self.socket = socket
        self.send_queue = asyncio.Queue()
        self.recv_queue = asyncio.Queue()
        self.read_task = None
        self.write_task = None
        self.timeout = 1
        self.message = None
        self.events = []
        self.stopped = False

    async def on_read(self, data):
        await self.recv_queue.put(data)

    async def on_write(self, data):
        pass

    async def event_loop(self):
        if self.stopped:
            return await self.stop()

        async def write():
            if not self.message:
                self.message = await self.send_queue.get()

            message = self.message
            _logger.debug("Sending message [%s]", self.message)
            await self.socket.send_json(self.message)
            _logger.debug("Message sent")
            self.message = None
            return message

        async def read():
            data = await self.socket.receive_json()
            _logger.debug("Read data %s", data)
            return data

        if not self.read_task:
            self.read_task = asyncio.ensure_future(read())

        if not self.write_task:
            self.write_task = asyncio.ensure_future(write())

        done, pending = await asyncio.wait(
            {self.read_task, self.write_task},
            timeout=self.timeout,
            return_when=asyncio.FIRST_COMPLETED
        )

        _logger.debug("Done Jobs %s %s", done, self.uuid)

        if self.read_task in done:
            try:
                self.events.append(
                    asyncio.ensure_future(
                        self.on_read(await self.read_task)
                    )
                )
            except Exception:
                self.stopped = True
            finally:
                self.read_task = None

        if self.write_task in done:
            self.events.append(
                asyncio.ensure_future(
                    self.on_write(await self.write_task)
                )
            )
            self.write_task = None

        if self.events:
            done, pending = await asyncio.wait(self.events, timeout=0.1)

            for task in done:
                await task

            # clean up all done events after
            to_remove = set()

            for event in self.events:
                if event.done():
                    to_remove.add(event)

            for event in to_remove:
                self.events.remove(event)

    async def stop(self):
        self.stopped = True
        await self.on_exit()

    async def on_exit(self):
        if self.read_task:
            self.read_task.cancel()
            self.read_task = None

        if self.write_task:
            self.write_task.cancel()
            self.write_task = None

        for task in self.events:
            task.cancel()

        self.events = []

        try:
            await self.socket.close()
        except Exception:
            _logger.error("Error closing socket")
