import socket
import asyncio
import logging
from pycolor import pycolor,setTermColor
from rich.table import Table
import time

class SocketClient:

    def __init__(self) -> None:
        self.recv = None
        self.lastData = {"Team":[None,0],"PlayerName":[None,0],"PlayerScore":[None,0],"Scored":[None,0],"Others":[None,0]}

    def assortData4UI(self,data) -> None:
        t = time.time()
        if data in ["end","init","f1","f0","f0n"]:
            self.lastData["Others"] = [data,t]
        elif data == "scored":
            self.lastData["Scored"] = [data,t]
        elif data[0] == "s":
            # Score
            self.lastData["PlayerScore"] = [data[1:].split(":")[1],t]
        elif data[0] == "p":
            # PlayerName
            self.lastData["PlayerName"] = [data[1:].split(":")[0],t]
        elif data[0] == "T":
            self.lastData["Team"] = [data,t]
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
        preRecv = ""
        while 1:
            loop = asyncio.get_event_loop()
            recv,_ = await loop.sock_recvfrom(s,256)
            self.recv = recv
            msg = recv.decode("utf-8")
            if msg == preRecv:
                continue
            logging.debug(msg)
            queue.put_nowait(msg)
            try:
                self.assortData4UI(msg)
            except:
                pass
            preRecv = msg

        socket.close()

if __name__ == "__main__":
    s = SocketClient()
    asyncio.run(s.main(asyncio.Queue()))