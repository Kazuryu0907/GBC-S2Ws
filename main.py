import asyncio
from socket_client import socketMain
from websocket_server import WebsockServ
import signal
import logging
from rich import print,box
from rich.console import Console,Group
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
import time
import random
#CTRL+Cで強制終了
signal.signal(signal.SIGINT,signal.SIG_DFL)
# logging.basicConfig(level=logging.DEBUG)

class WebsocketUI:
    """Display Webscoket UI(T/F)"""
    def __init__(self,websock:WebsockServ) -> None:
        self.websock = websock
        pass

    def __rich__(self) -> Panel:
        table = self.websock.createUITable()
        panel = Panel(
            Align.center(table,vertical="middle"),
            title="[b red]WebsocketUI",
        )
        return panel

def createHeaderPanel() -> Panel:
    grid = Table.grid(expand=True)
    grid.add_column(justify="center",ratio=1)
    grid.add_column(justify="right")
    grid.add_row(
        "Welcome Back!, [blue_violet]GBC-S2Ws!",
        "[red]ver 0.0.1"
    )
    panel = Panel(grid,style="")
    return panel

async def async_multi_sleep():
    layout = Layout()
    layout.split_column(
        Layout(name="upper",size=3),
        Layout(name="lower",size=10)
    )
    layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )

    layout["upper"].update(createHeaderPanel())
    queue = asyncio.Queue()
    websock = WebsockServ(queue=queue,layout=layout["lower"]["left"])

    layout["lower"]["right"].update(WebsocketUI(websock))

    layout["lower"]["left"].update(websock.createUITable())

    # print(layout)
    task1 = asyncio.create_task(socketMain(queue))
    task2 = asyncio.create_task(websock.main())
    with Live(layout) as live:
        # layout["lower"]["right"].update(WebsocketUI(websock))
        await asyncio.Future()



asyncio.run(async_multi_sleep())

