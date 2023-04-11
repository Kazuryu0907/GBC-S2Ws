import asyncio
from socket_client import SocketClient
from websocket_server import WebsockServ
from rich_layouts import WebsocketUI,Header,makeLayout,SocketUI,printLayout
import signal
import logging
from rich.live import Live
from rich.panel import Panel
from rich.console import Console

console = Console()
#CTRL+Cで強制終了
signal.signal(signal.SIGINT,signal.SIG_DFL)
logging.basicConfig(level=logging.DEBUG,filename="./test.log")
async def async_multi_sleep():
    layout = makeLayout()
    layout["upper"].update(Header())
    queue = asyncio.Queue()
    websock = WebsockServ(queue=queue)
    socket = SocketClient()

    layout["lower"]["right"].update(WebsocketUI(websock))
    # layout["main"].visible = False
    layout["lower"]["left"].update(SocketUI(socket))

    # print(layout)
    task1 = asyncio.create_task(socket.main(queue))
    task11 = asyncio.create_task(websock.sendDataFromQueue())
    task2 = asyncio.create_task(websock.websocketMain())
    task3 = asyncio.create_task(printLayout(layout))    

    
    await asyncio.Future()
    

try:
    asyncio.run(async_multi_sleep())
except Exception as e:
    console.print_exception(extra_lines=5,show_locals=True)
