import asyncio
import websockets
class WebsockServ:
    def __init__(self,queue:asyncio.Queue) -> None:
        self.queue = queue
        self.isConnected = False

    async def getQueue(self):
        print("hello queue")
        while 1:
            q:str = await self.queue.get()
            print(f"q;{q}")
            try:
                await self.websocket.send(q.encode().decode("unicode-escape"))
            except Exception as e:
                print(e)
                pass

    async def handler(self,websocket):
        self.websocket = websocket
        print("connected")
        async for msg in websocket:
            await websocket.send(msg)
        # asyncio.create_task(self.getQueue())

    async def web(self):
        print("web start")
        async with websockets.serve(self.handler,"localhost",8001):
            await asyncio.Future()#run forever

    async def main(self):
        task = asyncio.create_task(self.web())
        task2 = asyncio.create_task(self.getQueue())
        # await asyncio.gather(self.web(),asyncio.to_thread(self.getQueue))
    
if __name__ == "__main__":
    w = WebsockServ(asyncio.Queue())
    asyncio.run(w.web())