# -*- coding:utf-8 -*-
"""
    thread_asyncio_http.py
    ~~~~~~~~
    线程和协程, 异步 IO
    协程里不能加入阻塞 IO, 如果一定要, 可以将其放入线程池
    推荐!

    :author: Fufu, 2021/1/9
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

from util import run_perf, get_url, gen_url


@run_perf
def main(worker):
    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor(worker)

    tasks = [loop.run_in_executor(pool, get_url, *url) for url in gen_url(20, False)]
    res = loop.run_until_complete(asyncio.wait(tasks))

    loop.close()

    for x in res[0]:
        print(x.result())

    print('result:', res)


if __name__ == '__main__':
    # 0.26354289
    main(20)

    # 1.48266160
    # main(3)
