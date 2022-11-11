import os
import asyncio
import zmq
import zmq.asyncio
import logging


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
                    self.socket.send(b"false ot 1")
                else:
                    self.socket.send(b"Otvet ot 1")
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    env_port = os.environ.get("PORT", 9900)
    notifier = NotifierServer(int(env_port))

    async def run_all():
        await notifier.start()


    asyncio.run(run_all())
