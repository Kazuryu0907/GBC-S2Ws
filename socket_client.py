import socket
import asyncio
import logging
from pycolor import pycolor,setTermColor


async def socketMain(queue):
    logging.info(setTermColor("websocket start",pycolor.BLUE))
    host = ""
    port = 12345

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    s.setblocking(False)
    while 1:
        loop = asyncio.get_event_loop()
        recv,_ = await loop.sock_recvfrom(s,256)
        # logging.debug(recv.decode("utf-8"))
        msg = recv.decode("utf-8")
        queue.put_nowait(msg)

    socket.close()

if __name__ == "__main__":
    asyncio.run(socketMain(asyncio.Queue()))