import socket
import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor
def async_func(func):
    async def f(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
    return f


def sock(queue):
    print("sock start")
    host = ""
    port = 12345

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    while 1:
        recv,_ = s.recvfrom(256)
        print(recv.decode("utf-8"))
        queue.put_nowait(recv.decode("utf-8"))

    socket.close()

async def sock2(queue):
    print("sock start")
    host = ""
    port = 12345

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    s.setblocking(False)
    while 1:
        loop = asyncio.get_event_loop()
        recv,_ = await loop.sock_recvfrom(s,256)
        # recv,_ = await loop.run_in_executor(None,s.recvfrom,256)
        # print(recv.decode("utf-8"))
        queue.put_nowait(recv.decode("utf-8"))

    socket.close()

if __name__ == "__main__":
    asyncio.run(sock())