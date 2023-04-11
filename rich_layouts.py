from rich import print,box
from rich.console import Console,Group
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from websocket_server import WebsockServ
from socket_client import SocketClient

class Header:
    """
    Display Welcome Message & Version
    """
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

class WebsocketUI:
    """Display Webscoket UI(T/F)"""
    def __init__(self,websock:WebsockServ) -> None:
        self.websock = websock
        self.index = 0
        self.tick = 0
        self.TICKLIM = 5
        pass

    def __rich__(self) -> Panel:
        table = self.websock.createUITable()
        hourglass = [":hourglass:",":hourglass_flowing_sand:",":hourglass_not_done:",":hourglass_done:"]
        titleColor = 'red' if not self.websock.isAllConnected else 'green1'
        allow = list("="*self.TICKLIM)
        allow[self.tick] = "[white]>[/]"
        allowStr = f"[gray66]{''.join(allow)}[/]"
        panel = Panel(
            Align.center(table,vertical="middle"),
            title=f"[b {titleColor}][blue]GBC-S2Ws[/]{allowStr}Overlay[/] {hourglass[self.index] if not self.websock.isAllConnected else ':white_heavy_check_mark:'}",
            border_style="cyan"
        )
        
        self.index = 0 if self.index + 1 == len(hourglass) else self.index + 1
        self.tick = 0 if self.tick + 1 == self.TICKLIM else self.tick + 1

        return panel


class SocketUI:
    def __init__(self,socket:SocketClient) -> None:
        self.socket = socket
        self.preLastData = {}
        self.tick = 0
        self.TICKLIM = 5

    def __rich__(self) -> None:
        allow = list("="*self.TICKLIM)
        allow[self.tick] = "[white]>[/]"
        allowStr = f"[gray66]{''.join(allow)}[/]"
        panel = Panel(
            Align.center(self.createTable(),vertical="middle"),
            title=f"[b red][red]RL[/]{allowStr}[blue]GBC-S2Ws",
            border_style="cyan"
        )
        self.tick = 0 if self.tick + 1 == self.TICKLIM else self.tick + 1
        return panel
    
    def createTable(self):
        printTable = Table(header_style="b sea_green2")
        printTable.add_column("RL",justify="center")
        printTable.add_column("Connection Status",justify="center")
        for (key,d) in self.socket.lastData.items():
            printTable.add_row(f"[{'gray66' if d is None else 'cyan1'}]{key}",f"[{'gray66' if d is None else 'cyan1'}]{d}")
        return printTable

def makeLayout():
    layout = Layout()
    layout.split_column(
        Layout(name="upper",size=3),
        Layout(name="main",size=5),
        Layout(name="lower",size=10)
    )
    layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
    return layout

import asyncio
async def printLayout(layout):
    with Live(layout,refresh_per_second=4) as live:
        await asyncio.Future()
