# -*- coding:utf-8 -*-
"""
    aiohttp_http_limit.py
    ~~~~~~~~
    基于 asyncio 的 HTTP 框架, 并发限制方法示例
    推荐!!!

    :author: Fufu, 2021/1/9
"""
import aiohttp
import asyncio

from util import run_perf, gen_url


async def aio_get_url(url, sess):
    try:
        async with sess.get(url) as resp:
            return await resp.text()
    except Exception as e:
        return f'{url} {e}'


async def aio_get_url_sem(url, sem, sess):
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


async def aio_init(worker=100):
    """TCPConnector 连接池限制并发"""
    # limit 限制同时连接数, 默认是100, limit=0 无限制
    conn = aiohttp.TCPConnector(ssl=False, limit=worker)
    async with aiohttp.ClientSession(connector=conn) as sess:
        tasks = [asyncio.ensure_future(aio_get_url(url, sess)) for url in gen_url(20)]
        await run_tasks(tasks)


async def aio_init_sem(worker):
    """Semaphore 限制并发"""
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as sess:
        # 写在这儿
        sem = asyncio.Semaphore(worker)
        tasks = [asyncio.ensure_future(aio_get_url_sem(url, sem, sess)) for url in gen_url(20)]
        await run_tasks(tasks)


@run_perf
def main(worker):
    # 1.
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(aio_init(worker))

    # 2. Python 3.7+ aiohttp limit 限制并发
    # asyncio.run(aio_init(worker))

    # 3. Python 3.7+ Semaphore 限制并发, 推荐
    # Ref: https://docs.python.org/zh-cn/3/library/asyncio-task.html
    # 当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用。
    # 此函数总是会创建一个新的事件循环并在结束时关闭之。
    # 它应当被用作 asyncio 程序的主入口点，理想情况下应当只被调用一次。
    asyncio.run(aio_init_sem(worker))


if __name__ == '__main__':
    # 0.4903281
    # main(20)

    # 1.6397525
    main(3)
