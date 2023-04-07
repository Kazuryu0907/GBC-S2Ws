import asyncio
from socket_client import socketMain
from websocket_server import WebsockServ
import signal
import logging
#CTRL+Cで強制終了
signal.signal(signal.SIGINT,signal.SIG_DFL)
logging.basicConfig(level=logging.DEBUG)
async def async_multi_sleep():
    queue = asyncio.Queue()
    websock = WebsockServ(queue=queue)

    task1 = asyncio.create_task(socketMain(queue))
    task2 = asyncio.create_task(websock.main())

    await asyncio.Future()



asyncio.run(async_multi_sleep())

