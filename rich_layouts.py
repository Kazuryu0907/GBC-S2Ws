from rich import print,box
from rich.console import Console,Group
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from websocket_server import WebsockServ

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
