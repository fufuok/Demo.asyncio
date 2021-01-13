#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    aiphttp_vs_requests.py
    ~~~~~~~~
    同步和异步请求对比

    :author: Fufu, 2021/1/13
"""
import asyncio
import aiohttp
import requests

from util import run_perf, gen_url


def requests_get_url(url, sess):
    """使用 requests 请求 url (阻塞 IO)"""
    try:
        r = sess.get(url)
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        return f'{url} {e}'


async def aio_get_url(url, sess):
    try:
        async with sess.get(url) as resp:
            return await resp.text()
    except Exception as e:
        return f'{url} {e}'


async def aio_init():
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as sess:
        tasks = [aio_get_url(url, sess) for url in gen_url(20)]
        return await asyncio.wait(tasks)


@run_perf
def run_aiohttp():
    res = asyncio.run(aio_init())
    print('total:', len(res[0]), res)


@run_perf
def run_requests():
    sess = requests.Session()
    res = [requests_get_url(url, sess) for url in gen_url(20)]
    print('total:', len(res))


if __name__ == '__main__':
    # 1.030242
    run_aiohttp()

    # 5.0316202
    run_requests()
