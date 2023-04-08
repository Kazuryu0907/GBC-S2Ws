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
from rich.color import Color
import time
import random
#CTRL+Cで強制終了
signal.signal(signal.SIGINT,signal.SIG_DFL)
# logging.basicConfig(level=logging.DEBUG)

class WebsocketUI:
    """Display Webscoket UI(T/F)"""
    def __init__(self,websock:WebsockServ) -> None:
        self.websock = websock
        self.index = 0
        pass

    def __rich__(self) -> Panel:
        table = self.websock.createUITable()
        hourglass = [":hourglass:",":hourglass_flowing_sand:",":hourglass_not_done:",":hourglass_done:"]
        titleColor = 'red' if not self.websock.isAllConnected else 'green1'
        panel = Panel(
            Align.center(table,vertical="middle"),
            title=f"[b {titleColor}]WebsocketUI[/] {hourglass[self.index] if not self.websock.isAllConnected else ':white_heavy_check_mark:'}",
        )
        
        self.index = 0 if self.index + 1 == len(hourglass) else self.index + 1


        return panel

class Header:
    def __init__(self) -> None:
        self.index = 0
    def __rich__(self) -> Panel:
        maxIndex = 10
        earths = [":earth_africa:",":earth_americas:",":earth_asia:"]
        grid = Table.grid(expand=True)
        grid.add_column(justify="center",ratio=1)
        grid.add_column(justify="right")
        baseText = "[dark_orange]Welcome Back![/], [blue_violet]GBC-S2Ws!"
        text = f'[white]{"-"*self.index}[/]' + baseText + f'[white]{"-"*self.index}[/]'
        grid.add_row(
            text,
            "[red]ver 0.0.1"
        )
        panel = Panel(grid,style="")
        self.index = 0 if self.index + 1 == maxIndex else self.index + 1
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

    layout["upper"].update(Header())
    queue = asyncio.Queue()
    websock = WebsockServ(queue=queue)

    layout["lower"]["right"].update(WebsocketUI(websock))

    layout["lower"]["left"].update(websock.createUITable())

    # print(layout)
    task1 = asyncio.create_task(socketMain(queue))
    task2 = asyncio.create_task(websock.main())
    with Live(layout,refresh_per_second=4) as live:
        # layout["lower"]["right"].update(WebsocketUI(websock))
        await asyncio.Future()



asyncio.run(async_multi_sleep())

