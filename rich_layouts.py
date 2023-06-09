from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.tree import Tree

from websocket_server import WebsockServ
from socket_client import SocketClient
from datetime import datetime 

class Header:
    """
    Display Welcome Message & Version
    """
    def __init__(self,version) -> None:
        self.index = 0
        self.version = version

    def __rich__(self) -> Panel:
        maxIndex = 10

        grid = Table.grid(expand=True)
        # 中心にそろえる
        grid.add_column(justify="left")

        grid.add_column(justify="center",ratio=1)
        grid.add_column(justify="right")
        dashColor = "white"
        baseText = "[chartreuse2]Welcome Back!, GBC-S2Ws!"
        text = f'[{dashColor}]{"-"*self.index}[/]' + baseText + f'[{dashColor}]{"-"*self.index}[/]'
        grid.add_row(
            f"[black]{self.version}",
            text,
            f"[b dark_green]{self.version}"
        )
        panel = Panel(grid,border_style="cyan3")
        self.index = 0 if self.index + 1 == maxIndex else self.index + 1
        return panel
    
class Timer:
    """Display Timer UI"""
    def __rich__(self):
        panel = Panel(
            Align.center(f'[chartreuse2]{datetime.now().strftime(r"%Y/%m/%d %H:%M:%S").replace(":", "[blink]:[/]")}'),
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

    def __rich__(self) -> Panel:
        table = self.createUITable()
        clocks = [":twelve_o’clock:",":three_o’clock:",":six_o’clock:",":nine_o’clock:"]
        titleColor = 'red' if not self.websock.isAllConnected else 'green1'
        allow = list("="*self.TICKLIM)
        allow[self.tick] = "[white]>[/]"
        allowStr = f"[dark_cyan]{''.join(allow)}[/]"
        panel = Panel(
            Align.center(table,vertical="middle"),
            title=f"[b {titleColor}][dark_orange3]GBC-S2Ws[/]{allowStr}[deep_pink3]Overlay[/] {clocks[self.index] if not self.websock.isAllConnected else ':white_heavy_check_mark:'}",
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
        printTable = Table(show_header=True,header_style="bold chartreuse2")
        printTable.add_column("UI",justify="center")
        printTable.add_column("Connection Status",justify="center")
        UIs = ["/team","/icon","/playerName","/score","/transition"]
        self.websock.isAllConnected = True
        for UI in UIs:
            pathColor = 'chartreuse2' if UI in self.websock.connections.keys() else 'gray66'
            connectedEmojiStatus = "[chartreuse2]Connected[/]" if UI in self.websock.connections.keys() else "[gray66]None[/]"
            printTable.add_row(f"[{pathColor}]{UI[1:]}[/]",connectedEmojiStatus)
            # UIのTitle変更用
            if UI not in self.websock.connections.keys():
                self.websock.isAllConnected = False

        return printTable


class SocketUI:
    """Display SocketUI"""
    def __init__(self,socket:SocketClient) -> None:
        self.socket = socket
        self.preLastData = socket.lastData.copy()
        self.tick = 0
        self.TICKLIM = 5

    def __rich__(self) -> None:
        allow = list("="*self.TICKLIM)
        allow[self.tick] = "[white]>[/]"
        allowStr = f"[dark_cyan]{''.join(allow)}[/]"
        panel = Panel(
            Align.center(self.createTable(),vertical="middle"),
            title=f"[b red][deep_pink3]RL[/]{allowStr}[dark_orange3]GBC-S2Ws",
            border_style="cyan3"
        )
        self.tick = 0 if self.tick + 1 == self.TICKLIM else self.tick + 1
        return panel
    
    def createTable(self):
        """
        Create Socket UI Table.
        if received message, blink Table value 

        Returns
        -------
        printTable : rich.table.Table
            Created Socket UI
        """
        printTable = Table(show_header=True,header_style="b chartreuse2")
        printTable.add_column("RL",justify="center")
        printTable.add_column("Connection Status",justify="center")
        # 変更あり=>orange_red1 None=>gray66 otherwise=>cyan1
        color = lambda d,key:'gray66' if d[0] is None else 'chartreuse2' if d[1] == self.preLastData[key][1] else 'deep_pink3'
        
        for (key,d) in self.socket.lastData.items():
            printTable.add_row(f"[{color(d,key)}]{key}",f"[{color(d,key)}]{d[0]}")
        
        self.preLastData = self.socket.lastData.copy()
        return printTable

class SimedPathUI:
    """Display Similary Path"""
    def __init__(self,websock:WebsockServ) -> None:
        self.websock = websock
        
    def __rich__(self):
        printTree = Tree(f"[chartreuse2]{self.websock.lastRawIcon}")
        simIcons = self.websock.lastSimIcons.copy()
        for i in range(min(10-2,len(simIcons))):
            fname,per,index = list(simIcons[i])
            color = "dark_orange3" if i == 0 else "white"
            printTree.add(f"[chartreuse2]{fname}:[{color}]{round(per,2)}%")

        return Panel(Align.center(printTree),title="[dark_orange3]Icon Similary",border_style="cyan3")

class IconsUI:
    """Display Icon Files"""
    def __init__(self,websock:WebsockServ) -> None:
        self.sim = websock.similary
        self.fileNames = self.sim.fileNamesEx.copy()
        self.index = 0
        self.WIDTH = 10-2
        self.fileLen = len(self.fileNames)
        self.cushion = 0
        self.MaxCushion = 3

    def __rich__(self):
        printTable = Table(show_header=False,show_edge=False)
        printTable.add_column(f"[dark_orange3]Files:[chartreuse2]{self.fileLen}",style="chartreuse2")
        calcMod = lambda x:x % self.fileLen
        zeroColor = lambda x: "dark_orange3" if x == 1 else "white" 
        for i in range(self.WIDTH):
            printTable.add_row(f"[white][{zeroColor(calcMod(i+self.index)+1)}]{calcMod(i+self.index)+1}[/]:[/] {self.fileNames[calcMod(i+self.index)]}")
        
        self.cushion += 1
        if self.cushion == self.MaxCushion:
            self.cushion = 0
            self.index = 0 if self.index + 1 == self.fileLen else self.index + 1
        return Panel(Align.center(printTable),title=f"[dark_orange3]Loaded Icon Files:[chartreuse2] {self.fileLen}",border_style="cyan3")

class SimedTeamPathUI:
    """Display Similary Path"""
    def __init__(self,websock:WebsockServ) -> None:
        self.websock = websock
        
    def __rich__(self):
        printTree = Tree(f"[chartreuse2]{self.websock.lastRawTeam}")
        simTeams = self.websock.lastSimTeams.copy()
        for i in range(min(10-2,len(simTeams))):
            fname,per,_ = list(simTeams[i])
            color = "dark_orange3" if i == 0 else "white"
            printTree.add(f"[chartreuse2]{fname}:[{color}]{round(per,2)}%")

        return Panel(Align.center(printTree),title="[dark_orange3]Team Similary",border_style="cyan3")

class TeamsUI:
    """Display Icon Files"""
    def __init__(self,websock:WebsockServ) -> None:
        self.sim = websock.similaryTeam
        self.fileNames = self.sim.fileNamesEx.copy()
        self.index = 0
        self.WIDTH = 10-2
        self.fileLen = len(self.fileNames)
        self.cushion = 0
        self.MaxCushion = 3

    def __rich__(self):
        printTable = Table(show_header=False,show_edge=False)
        printTable.add_column(f"[dark_orange3]Files:[chartreuse2]{self.fileLen}",style="chartreuse2")
        calcMod = lambda x:x % self.fileLen
        zeroColor = lambda x: "dark_orange3" if x == 1 else "white" 
        for i in range(self.WIDTH):
            printTable.add_row(f"[white][{zeroColor(calcMod(i+self.index)+1)}]{calcMod(i+self.index)+1}[/]:[/] {self.fileNames[calcMod(i+self.index)]}")
        
        self.cushion += 1
        if self.cushion == self.MaxCushion:
            self.cushion = 0
            self.index = 0 if self.index + 1 == self.fileLen else self.index + 1
        return Panel(Align.center(printTable),title=f"[dark_orange3]Loaded Team Files:[chartreuse2] {self.fileLen}",border_style="cyan3")

def makeLayout():
    """Create Layout"""
    layout = Layout()
    layout.split_column(
        Layout(name="upper",size=3),
        Layout(name="main",size=3),
        Layout(name="lower",size=11),
        Layout(name="bot",size=6),
        Layout(name="team",size=6),
    )
    layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
    layout["bot"].split_row(
            Layout(name="left"),
            Layout(name="right")
    )
    layout["team"].split_row(
            Layout(name="left"),
            Layout(name="right")
    )
    return layout
