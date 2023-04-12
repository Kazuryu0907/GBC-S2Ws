from rich import print,box
from rich.console import Console,Group
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from websocket_server import WebsockServ
from socket_client import SocketClient
from datetime import datetime 

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
        # 中心にそろえる
        grid.add_column(justify="left")

        grid.add_column(justify="center",ratio=1)
        grid.add_column(justify="right")
    
        baseText = "[dark_orange]Welcome Back![/], [blue_violet]GBC-S2Ws!"
        text = f'[white]{"-"*self.index}[/]' + baseText + f'[white]{"-"*self.index}[/]'
        grid.add_row(
            "[black]ver 0.0.1",
            text,
            "[b red]ver 0.0.1"
        )
        panel = Panel(grid,border_style="cyan3")
        self.index = 0 if self.index + 1 == maxIndex else self.index + 1
        return panel
    
class Timer:
    def __rich__(self):
        panel = Panel(
            Align.center(f'[dark_orange]{datetime.now().strftime(r"%Y/%m/%d %H:%M:%S").replace(":", "[blink]:[/]")}'),
            border_style="cyan3"
            )
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
        table = self.createUITable()
        hourglass = [":hourglass:",":hourglass_flowing_sand:",":hourglass_not_done:",":hourglass_done:"]
        clocks = [":twelve_o’clock:",":three_o’clock:",":six_o’clock:",":nine_o’clock:"]
        titleColor = 'red' if not self.websock.isAllConnected else 'green1'
        allow = list("="*self.TICKLIM)
        allow[self.tick] = "[white]>[/]"
        allowStr = f"[gray66]{''.join(allow)}[/]"
        panel = Panel(
            Align.center(table,vertical="middle"),
            title=f"[b {titleColor}][blue]GBC-S2Ws[/]{allowStr}Overlay[/] {clocks[self.index] if not self.websock.isAllConnected else ':white_heavy_check_mark:'}",
            border_style="cyan3"
        )
        
        self.index = 0 if self.index + 1 == len(clocks) else self.index + 1
        self.tick = 0 if self.tick + 1 == self.TICKLIM else self.tick + 1

        return panel

    def createUITable(self) -> Table:
        """
        Create Websocket UI Table.
        When all plugin is connected, self.isAllConnected will be "True" 

        Returns
        -------
        printTable : rich.table.Table
            Created Websocket UI
        """
        printTable = Table(show_header=True,header_style="bold cyan3")
        printTable.add_column("UI",justify="center")
        printTable.add_column("Connection Status",justify="center")
        UIs = ["/icon","/playerName","/score","/transition"]
        self.websock.isAllConnected = True
        for UI in UIs:
            pathColor = 'cyan1' if UI in self.websock.connections.keys() else 'gray66'
            connectedEmojiStatus = "[green]:white_check_mark:[/]" if UI in self.websock.connections.keys() else "[red]:cross_mark:[/]"
            printTable.add_row(f"[{pathColor}]{UI[1:]}[/]",connectedEmojiStatus)
            # UIのTitle変更用
            if UI not in self.websock.connections.keys():
                self.websock.isAllConnected = False

        return printTable


class SocketUI:
    def __init__(self,socket:SocketClient) -> None:
        self.socket = socket
        self.preLastData = socket.lastData.copy()
        self.tick = 0
        self.TICKLIM = 5

    def __rich__(self) -> None:
        allow = list("="*self.TICKLIM)
        allow[self.tick] = "[white]>[/]"
        allowStr = f"[gray66]{''.join(allow)}[/]"
        panel = Panel(
            Align.center(self.createTable(),vertical="middle"),
            title=f"[b red][red]RL[/]{allowStr}[blue]GBC-S2Ws",
            border_style="cyan3"
        )
        self.tick = 0 if self.tick + 1 == self.TICKLIM else self.tick + 1
        return panel
    
    def createTable(self):
        printTable = Table(show_header=True,header_style="b cyan3")
        printTable.add_column("RL",justify="center")
        printTable.add_column("Connection Status",justify="center")
        # 変更あり=>orange_red1 None=>gray66 otherwise=>cyan1
        color = lambda d,key:'gray66' if d is None else 'cyan1' if d == self.preLastData[key] else 'orange_red1'
        
        for (key,d) in self.socket.lastData.items():
            printTable.add_row(f"[{color(d,key)}]{key}",f"[{color(d,key)}]{d}")
        
        self.preLastData = self.socket.lastData.copy()
        return printTable

def makeLayout():
    layout = Layout()
    layout.split_column(
        Layout(name="upper",size=3),
        Layout(name="main",size=3),
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
