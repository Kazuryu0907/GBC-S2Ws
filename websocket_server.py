import asyncio
import websockets
import logging
from pycolor import pycolor,setTermColor
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import print
from rich.layout import Layout
from rich.panel import Panel
import random

class WebsockServ:
    def __init__(self,queue:asyncio.Queue) -> None:
        self.queue = queue
        self.isConnected = False
        self.connections = {}
        self.console = Console()
        self.isUpdatebleTable = True

    async def sendQueue(self) -> None:
        while 1:
            q:str = await self.queue.get()
            logging.debug(f"< Queue:{q}")
            # Null文字除去
            q = q.encode().replace(b"\x00",b"").decode()
            try:
                if q == "scored":
                    await self.connections["/transition"].send(q)
                elif q[0] == "s":
                    await self.connections["/score"].send(q)
                elif q[0] == "p":
                    await self.connections["/playerName"].send(q)
                    await self.connections["/icon"].send(q)
                # for s in self.connections.copy():
                #     await s.send(q.encode().decode("unicode-escape"))
                #     await asyncio.sleep(0)
                # websockets.broadcast(self.connections,q.encode().decode("unicode-escape"))
            except Exception as e:
                # logging.error(setTermColor("ブラウザ接続待機中...",pycolor.GREEN))
                # logging.error(e)
                pass

    def createUITable(self) -> Table:
        """
        Create Websocket UI Table.
        When all plugin is connected, self.isAllConnected will be "True" 
        """
        printTable = Table(show_header=True,header_style="bold sea_green2")
        printTable.add_column("UI",justify="center")
        printTable.add_column("Connection Status",justify="center")
        UIs = ["/icon","/playerName","/score","/transition"]
        self.isAllConnected = True
        for UI in UIs:
            printTable.add_row(f"[{'cyan1' if UI in self.connections.keys() else 'gray66'}]{UI[1:]}[/]","[green]:white_check_mark:[/]" if UI in self.connections.keys() else "[red]:cross_mark:[/]")
            if UI not in self.connections.keys():
                self.isAllConnected = False
        return printTable
    
    async def handler(self,websocket) -> None:
        self.websocket = websocket
        self.connections[websocket.path] = websocket
        # (self.connections)
        logging.info(setTermColor(f"connected:{websocket.path}",pycolor.BLUE))
        #  Table更新
        self.isUpdatebleTable = True
        # ここ消したら接続切れるぞ
        async for msg in websocket:
            await websocket.send(msg)
            await asyncio.sleep(0)
        try:
            await websocket.wait_closed()
        finally:
            self.connections.pop(websocket.path)
            # 切断時Table更新
            self.isUpdatebleTable = True

    async def websocketMain(self) -> None:
        logging.info(setTermColor("web start",pycolor.BLUE))
        async with websockets.serve(self.handler,"localhost",8001):
            await asyncio.Future()#run forever

    async def main(self) -> None:
        task = asyncio.create_task(self.websocketMain())
        task2 = asyncio.create_task(self.sendQueue())

