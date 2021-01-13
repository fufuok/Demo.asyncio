# -*- coding:utf-8 -*-
"""
    thread_asyncio_requests_done.py
    ~~~~~~~~
    requests(未加载 Monkey-patch)
    线程和协程, 异步 IO
    协程里不能加入阻塞 IO, 如果一定要, 可以将其放入线程池
    推荐!!!

    :author: Fufu, 2021/1/9
"""
import asyncio
from requests import Session
from concurrent.futures import ThreadPoolExecutor

from util import run_perf, gen_url


def requests_get_url(url, sess):
    """使用 requests 请求 url (阻塞 IO)"""
    try:
        r = sess.get(url)
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        return f'{url} {e}'


async def run_tasks(tasks):
    """即时获取任务结果"""
    for task in asyncio.as_completed(tasks):
        html = await task
        print('...' * 100, html)


@run_perf
def main(max_worker):
    sess = Session()

    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor(max_worker)

    tasks = [loop.run_in_executor(pool, requests_get_url, url, sess) for url in gen_url(20)]
    loop.run_until_complete(run_tasks(tasks))

    loop.close()


if __name__ == '__main__':
    # 0.3171138
    main(20)

    # 1.5930275
    # main(3)
