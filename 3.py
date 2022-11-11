import json
import os

import asyncio
import zmq
import zmq.asyncio

import typing as t
import logging


class NotificationClient():
    def __init__(self, host: t.Optional[str] = None, port: t.Optional[int] = None):
        timeout = 500000
        self.ctx = zmq.asyncio.Context()
        self.ctx.setsockopt(zmq.SNDTIMEO, timeout)
        self.ctx.setsockopt(zmq.RCVTIMEO, timeout)
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.connect(f"tcp://{host}:{port}")

    async def send_without_template(self):
        try:
            await self.socket.send(b'Zapros ot 3')
            msg = await self.socket.recv()
            if msg:
                print(msg)
        except zmq.ZMQError:
            raise Exception('Server is not available')


if __name__ == "__main__":

    async def run_all():
        a = NotificationClient(port=9900, host='localhost')
        await a.send_without_template()


    asyncio.run(run_all())
