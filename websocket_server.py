import asyncio
import websockets
import logging
from pycolor import pycolor,setTermColor
from rich.table import Table
import glob
import os
from rapidfuzz.process import extract


class SimilaryFile:
    def __init__(self,path:str) -> None:
        files = glob.glob(path)
        self.fileNames = list(map(lambda f:os.path.basename(f).split(".")[0],files))
        self.nameFileTable = {f"{n}":f for (f,n) in list(zip(files,self.fileNames))}
        self.fileNamesEx = list(map(lambda f:os.path.basename(f),files))

    def getSimilaryPath(self,query:str):
        similary = extract(query,self.fileNames,limit=10)
        mostSimilaryName = list(similary[0])[0]
        self.sims = similary
        return self.nameFileTable[mostSimilaryName]


class WebsockServ:
    """
    Websocket Server 4 GBC-S2Ws
    """
    def __init__(self,queue:asyncio.Queue,simPath:str) -> None:
        """
        Parameters
        ----------
        queue : asyncio.Queue
            Queue from Socket.
        """
        self.queue = queue
        self.isConnected = False
        self.connections = {}
        self.isUpdatebleTable = True
        self.similary = SimilaryFile(simPath)
        self.lastRawIcon = "None"
        self.lastSimIcons = []

    async def sendDataFromQueue(self) -> None:
        """
        Get Queue from Socket and send assorted data to Websocket. 
        """
        while 1:
            q:str = await self.queue.get()
            # logging.debug(f"< Queue:{q}")
            # Null文字除去
            q = q.encode().replace(b"\x00",b"").decode()
            try:
                if q == "scored":
                    await self.connections["/transition"].send(q)
                elif q[0] == "s":
                    await self.connections["/score"].send(q)
                elif q[0] == "p":
                    self.lastRawIcon,index = q[1:].split(":")
                    simedPath = self.similary.getSimilaryPath(self.lastRawIcon)
                    self.lastSimIcons = self.similary.sims
                    await self.connections["/playerName"].send(q)
                    await self.connections["/icon"].send(f"p:{simedPath}:{index}")
            except Exception as e:
                # logging.error(setTermColor("ブラウザ接続待機中...",pycolor.GREEN))
                logging.debug(e)
                pass

    def createUITable(self) -> Table:
        """
        Create Websocket UI Table.
        When all plugin is connected, self.isAllConnected will be "True" 

        Returns
        -------
        printTable : rich.table.Table
            Created Websocket UI
        """
        printTable = Table(show_header=True,header_style="bold sea_green2")
        printTable.add_column("UI",justify="center")
        printTable.add_column("Connection Status",justify="center")
        UIs = ["/icon","/playerName","/score","/transition"]
        self.isAllConnected = True
        for UI in UIs:
            pathColor = 'cyan1' if UI in self.connections.keys() else 'gray66'
            connectedEmojiStatus = "[green]:white_check_mark:[/]" if UI in self.connections.keys() else "[red]:cross_mark:[/]"
            printTable.add_row(f"[{pathColor}]{UI[1:]}[/]",connectedEmojiStatus)
            # UIのTitle変更用
            if UI not in self.connections.keys():
                self.isAllConnected = False

        return printTable
    
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