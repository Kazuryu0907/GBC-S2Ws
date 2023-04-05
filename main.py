import asyncio
from client import sock,sock2
from webs import WebsockServ
import signal

from concurrent.futures import ProcessPoolExecutor
signal.signal(signal.SIGINT,signal.SIG_DFL)
asyncio.get_event_loop().set_debug(1)

async def async_multi_sleep():
    queue = asyncio.Queue()
    webs = WebsockServ(queue=queue)
    # task1 = asyncio.create_task(asyncio.to_thread(sock,queue))
    task1 = asyncio.create_task(sock2(queue))
    task2 = asyncio.create_task(webs.main())
    # while not webs.isConnected:
    #     print(f"con:{webs.isConnected}")
    # task3 = asyncio.create_task(queuegetter(queue,webs))
    # task3 = asyncio.create_task(asyncio.to_thread(queuegetter,queue,webs))
    await asyncio.Future()
    # await task1
    # await task2
    # await task3
    #並列処理　例外でも継続
    # await asyncio.gather(*co_list)
    # tasks.append(asyncio.create_task(sock()))


asyncio.run(async_multi_sleep())

