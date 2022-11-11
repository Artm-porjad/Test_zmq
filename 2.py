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
            await self.socket.send(b'Zapros ot 2')
            msg = await self.socket.recv()
            if msg:
                print(msg)
        except zmq.ZMQError:
            raise Exception('Server is not available')


class NotifierServer():
    def __init__(self, port: int):
        ctx = zmq.asyncio.Context()
        self.socket = ctx.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % port)
        logging.info(f'listen on 0.0.0.0:{port}')

    async def start(self):
        while True:
            try:
                msg = await self.socket.recv()
                try:
                    print(msg)
                except Exception as e:
                    logging.error(e)
                    self.socket.send(b"false ot 2")
                else:
                    self.socket.send(b"Otvet ot 2")
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    env_port = os.environ.get("PORT", 9901)
    notifier = NotifierServer(int(env_port))


    async def run_all():
        await notifier.start()
        a = NotificationClient(port=9900, host='localhost')
        await a.send_without_template()


    asyncio.run(run_all())
