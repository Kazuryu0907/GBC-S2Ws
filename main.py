import asyncio
from socket_client import socketMain
from websocket_server import WebsockServ
from rich_layouts import WebsocketUI,Header,makeLayout
import signal
import logging
from rich.live import Live

#CTRL+Cで強制終了
signal.signal(signal.SIGINT,signal.SIG_DFL)
# logging.basicConfig(level=logging.DEBUG)

async def async_multi_sleep():
    layout = makeLayout()
    layout["upper"].update(Header())
    queue = asyncio.Queue()
    websock = WebsockServ(queue=queue)

    layout["lower"]["right"].update(WebsocketUI(websock))

    # layout["lower"]["left"].update(websock.createUITable())

    # print(layout)
    task1 = asyncio.create_task(socketMain(queue))
    task2 = asyncio.create_task(websock.main())
    with Live(layout,refresh_per_second=4) as live:
        # layout["lower"]["right"].update(WebsocketUI(websock))
        await asyncio.Future()



asyncio.run(async_multi_sleep())

