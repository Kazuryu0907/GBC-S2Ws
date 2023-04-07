import asyncio
from socket_client import socketMain
from websocket_server import WebsockServ
import signal
import logging
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
import time
#CTRL+Cで強制終了
signal.signal(signal.SIGINT,signal.SIG_DFL)
# logging.basicConfig(level=logging.DEBUG)
async def async_multi_sleep():
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
    layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
    layout["upper"].update(Panel("Welcome!",title="Welcome Back!, [blue_violet]GBC-S2Ws!",title_align="center"))
    queue = asyncio.Queue()
    websock = WebsockServ(queue=queue,layout=layout["lower"]["left"])
    # layout["lower"]["left"].update(websock.createUITable())


    print(layout)
    task1 = asyncio.create_task(socketMain(queue))
    task2 = asyncio.create_task(websock.main())
    # print(Panel.fit("Welcome Back!, [blue_violet]GBC-S2Ws!"))
    await asyncio.Future()



asyncio.run(async_multi_sleep())

