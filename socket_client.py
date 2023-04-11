import socket
import asyncio
import logging
from pycolor import pycolor,setTermColor
from rich.table import Table


class SocketClient:

    def __init__(self) -> None:
        self.recv = None
        self.lastData = {"PlayerName":None,"PlayerScore":None,"Scored":None,"Others":None}

    def assortData4UI(self,data) -> None:
        if data in ["scored","end","init"]:
            self.lastData["Others"] = data
        elif data == "scored":
            # self.lastData["scored"] = data
            pass
        elif data[0] == "s":
            # Score
            self.lastData["PlayerScore"] = data[1:].split(":")[1]
        elif data[0] == "p":
            # PlayerName
            self.lastData["PlayerName"] = data[1:].split(":")[0]


    def createSocketTable(self):
        printTable = Table(header_style="b sea_green2")
        printTable.add_column("RL",justify="center")
        printTable.add_column("Connection Status",justify="center")
        printTable.add_row("A",":white_check_mark:")
        return printTable

    async def main(self,queue):
        """
        Create Socket Client & On recved message,Put data to Queue.

        Parameters:
        queue : asyncio.Queue
            Queue for Websocket server.
        """
        logging.info(setTermColor("socket start",pycolor.BLUE))
        host = ""
        port = 12345

        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((host,port))
        s.setblocking(False)

        while 1:
            loop = asyncio.get_event_loop()
            recv,_ = await loop.sock_recvfrom(s,256)
            self.recv = recv
            # logging.debug(recv.decode("utf-8"))
            msg = recv.decode("utf-8")
            queue.put_nowait(msg)
            self.assortData4UI(msg)

        socket.close()

if __name__ == "__main__":
    s = SocketClient()
    asyncio.run(s.main(asyncio.Queue()))