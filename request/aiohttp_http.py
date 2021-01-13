# -*- coding:utf-8 -*-
"""
    aiohttp_http.py
    ~~~~~~~~
    基于 asyncio 的 HTTP 框架
    推荐!!

    :author: Fufu, 2021/1/9
"""
import aiohttp
import asyncio

from util import run_perf, gen_url


async def aio_get_url(url, sem):
    async with sem:
        async with aiohttp.ClientSession() as sess:
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


@run_perf
def main(worker):
    # 并发限制
    sem = asyncio.Semaphore(worker)

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(aio_get_url(url, sem)) for url in gen_url(20)]

    # 1.
    loop.run_until_complete(run_tasks(tasks))

    # 2.
    # res = loop.run_until_complete(asyncio.gather(*tasks))
    # for x in res:
    #     print(x)
    # print('all completed:', res)

    # 3.
    # res = loop.run_until_complete(asyncio.wait(tasks))
    # for task in tasks:
    #     print(task.result())
    # print('all completed:', res)

    # 4.
    # res = loop.run_until_complete(asyncio.wait([aio_get_url(url, sem) for url in gen_url(20)]))
    # for task in res[0]:
    #     print(task.result())
    # print('all completed:', res)

    loop.close()


if __name__ == '__main__':
    # 0.4935275
    main(20)

    # 1.48266160
    # main(3)
