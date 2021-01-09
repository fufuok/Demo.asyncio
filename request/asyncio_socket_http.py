# -*- coding:utf-8 -*-
"""
    asyncio_socket_http.py
    ~~~~~~~~
    异步 IO socket

    :author: Fufu, 2021/1/9
"""
import asyncio

from util import run_perf, async_get_url, gen_url


async def limit_req(url, sem):
    async with sem:
        return await async_get_url(*url)


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
    tasks = [asyncio.ensure_future(limit_req(url, sem)) for url in gen_url(20, False)]

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
    # res = loop.run_until_complete(asyncio.wait([limit_req(url, sem) for url in gen_url(20, False)]))
    # for task in res[0]:
    #     print(task.result())
    # print('all completed:', res)


if __name__ == '__main__':
    # 0.56679879
    main(20)

    # 1.6877445
    # main(3)
