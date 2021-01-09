# -*- coding:utf-8 -*-
"""
    thread_asyncio_http_done.py
    ~~~~~~~~
    线程和协程, 异步 IO
    协程里不能加入阻塞 IO, 如果一定要, 可以将其放入线程池
    推荐!!

    :author: Fufu, 2021/1/9
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

from util import run_perf, get_url, gen_url


async def run_tasks(tasks):
    """完成一个即打印一个"""
    for task in asyncio.as_completed(tasks):
        html = await task
        print('...' * 100, html)


@run_perf
def main(max_worker):
    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor(max_worker)

    tasks = [loop.run_in_executor(pool, get_url, *url) for url in gen_url(20, False)]
    loop.run_until_complete(run_tasks(tasks))

    loop.close()


if __name__ == '__main__':
    # 0.2970545
    main(20)

    # 1.48266160
    # main(3)
