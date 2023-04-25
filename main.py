import asyncio
import signal
import logging
from rich.live import Live
from rich.console import Console
from socket_client import SocketClient
from websocket_server import WebsockServ
from rich_layouts import WebsocketUI,Header,makeLayout,SocketUI,Timer,SimedPathUI,IconsUI
from similary_file import SimilaryFile

console = Console()
#CTRL+Cで強制終了
signal.signal(signal.SIGINT,signal.SIG_DFL)
logging.basicConfig(level=logging.DEBUG,filename="./test.log")
async def async_multi_sleep():

    layout = makeLayout()
    
    queue = asyncio.Queue()
    simPath = "./graphics/images/*"
    sim = SimilaryFile(simPath)
    websock = WebsockServ(queue,sim)
    socket = SocketClient()

    layout["upper"].update(Header())
    layout["main"].update(Timer())
    layout["lower"]["right"].update(WebsocketUI(websock))
    layout["lower"]["left"].update(SocketUI(socket))
    layout["bot"]["left"].update(SimedPathUI(websock))
    layout["bot"]["right"].update(IconsUI(websock))

    task1 = asyncio.create_task(socket.main(queue))
    task11 = asyncio.create_task(websock.sendDataFromQueue())
    task2 = asyncio.create_task(websock.websocketMain())
    with Live(layout,refresh_per_second=4) as live:
        await asyncio.Future()    
    

try:
    asyncio.run(async_multi_sleep())
except Exception as e:
    console.print_exception(extra_lines=5,show_locals=True)
