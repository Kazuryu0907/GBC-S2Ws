import asyncio
import websockets
import logging
from pycolor import pycolor,setTermColor
from rich.table import Table
from similary_file import SimilaryFile


class WebsockServ:
    """
    Websocket Server 4 GBC-S2Ws
    """
    def __init__(self,queue:asyncio.Queue,sim:SimilaryFile) -> None:
        """
        Parameters
        ----------
        queue : asyncio.Queue
            Queue from Socket.
        sim : SimilaryFile
            SimilaryFile instance.
        """
        self.queue = queue
        self.isConnected = False
        self.connections = {}
        self.isUpdatebleTable = True
        self.similary = sim
        self.lastRawIcon = "None"
        self.lastSimIcons = []

    async def sendDataFromQueue(self) -> None:
        """
        Get Queue from Socket and send assorted data to Websocket. 
        """
        async def stream(msg:str):
            await self.connections["/boost"].send(msg)
        lastq = ""
        while 1:
            q:str = await self.queue.get()
            # logging.debug(f"< Queue:{q}")
            # Null文字除去
            q = q.encode().replace(b"\x00",b"").decode()
            if q == lastq:
                continue
            try:
                if q == "scored":
                    await self.connections["/transition"].send(q)
                elif q[0] == "t":
                    await self.connections["/boost"].send(q)
                elif q[0] == "T":
                    await self.connections["/boost"].send(q)
                elif q[0] == "b":
                    await self.connections["/boost"].send(q)
                elif q == "f0":
                    await stream("hidden")
                elif q == "f1":
                    await stream("visible")
                elif q == "end":
                    await stream("reset")
                

            except Exception as e:
                # logging.error(setTermColor("ブラウザ接続待機中...",pycolor.GREEN))
                logging.debug(e)
                pass

            lastq = q
    
    async def handler(self,websocket) -> None:
        """
        Handler for Websocket.(called when new socket connected)

        Parameters
        ----------
        websocket : websocket
            websocket.
        """
        self.websocket = websocket
        self.connections[websocket.path] = websocket

        logging.info(setTermColor(f"connected:{websocket.path}",pycolor.BLUE))
        #  Table更新
        self.isUpdatebleTable = True
        # ここ消したら接続切れるぞ
        async for msg in websocket:
            await websocket.send(msg)
            await asyncio.sleep(0)

        try:
            await websocket.wait_closed()
        except Exception as e:
            logging.error(e)
        finally:
            self.connections.pop(websocket.path)
            # 切断時Table更新
            self.isUpdatebleTable = True
            

    async def websocketMain(self) -> None:
        """
        Init function for this class.
        Run server.
        """
        logging.info(setTermColor("Websocket start",pycolor.BLUE))
        async with websockets.serve(self.handler,"localhost",8001):
            await asyncio.Future()#run forever

    async def main(self) -> None:
        """
        Run server & Send data to Web-browser
        """
        task = asyncio.create_task(self.websocketMain())
        task2 = asyncio.create_task(self.sendDataFromQueue())

if __name__ == "__main__":
    a = SimilaryFile("./graphics/images/*")
    print(a.getSimilaryPath("aaa"))