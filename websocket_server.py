import asyncio
import websockets
import logging
from pycolor import pycolor,setTermColor

class WebsockServ:
    def __init__(self,queue:asyncio.Queue) -> None:
        self.queue = queue
        self.isConnected = False
        self.connections = set()

    async def sendQueue(self) -> None:
        while 1:
            q:str = await self.queue.get()
            logging.debug(f"q;{q}")
            try:
                websockets.broadcast(self.connections,q.encode().decode("unicode-escape"))
            except Exception as e:
                logging.error(setTermColor("ブラウザ接続待機中...",pycolor.GREEN))
                logging.error(e)
                pass

    async def handler(self,websocket) -> None:
        self.websocket = websocket
        self.connections.add(websocket)
        logging.info(setTermColor("connected",pycolor.BLUE))
        # ここ消したら接続切れるぞ
        async for msg in websocket:
            await websocket.send(msg)
        try:
            await websocket.wait_closed()
        finally:
            self.connections.remove(websocket)

    async def websocketMain(self) -> None:
        logging.info(setTermColor("web start",pycolor.BLUE))
        async with websockets.serve(self.handler,"localhost",8001):
            await asyncio.Future()#run forever

    async def main(self) -> None:
        task = asyncio.create_task(self.websocketMain())
        task2 = asyncio.create_task(self.sendQueue())
