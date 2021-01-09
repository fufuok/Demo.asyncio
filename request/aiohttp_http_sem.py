# -*- coding:utf-8 -*-
"""
    aiohttp_http_sem.py
    ~~~~~~~~
    基于 asyncio 的 HTTP 框架
    推荐!!!

    :author: Fufu, 2021/1/9
"""
import aiohttp
import asyncio

from util import run_perf, gen_url


async def aio_get_url(url, sem, sess):
    async with sem:
        try:
            async with sess.get(url) as resp:
                return await resp.text()
        except Exception as e:
            return f'{url} {e}'


async def run_tasks(tasks):
    """即时获取任务结果"""
    for task in asyncio.as_completed(tasks):
        res = await task
        print('completed:', res)


async def aio_init(sem):
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as sess:
        tasks = [asyncio.ensure_future(aio_get_url(url, sem, sess)) for url in gen_url(20)]
        await run_tasks(tasks)
        # return await asyncio.gather(*tasks)


@run_perf
def main(worker):
    # 并发限制
    sem = asyncio.Semaphore(worker)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(aio_init(sem))


if __name__ == '__main__':
    # 0.4903281
    main(20)

    # 1.6397525
    # main(3)
