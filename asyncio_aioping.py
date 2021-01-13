#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    asyncio_aioping.py
    ~~~~~~~~
    协程, 异步 IO
    (不如系统 PING 命令稳定)

    https://github.com/stellarbit/aioping

    :author: Fufu, 2019/11/3
"""
import threading
import time
import asyncio
import aioping


def producer():
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        ips = f.read().strip().split('\n')
        return ips


async def consumer(ip, timeout=3):
    """消费者, PING IP"""
    print('--- is consumer', ip, threading.currentThread())
    try:
        delay = await aioping.ping(ip, timeout=timeout) * 1000
        return ip, delay
    except TimeoutError:
        return ip, 0


async def run_tasks(tasks):
    """完成一个即打印一个"""
    for task in asyncio.as_completed(tasks):
        res = await task
        print('completed:', res)


def main():
    stime = time.perf_counter()

    ips = producer()
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(consumer(ip, 3)) for ip in ips for i in range(5)]

    loop.run_until_complete(run_tasks(tasks))

    # res = loop.run_until_complete(asyncio.gather(*tasks))
    # print('all completed:', res)

    loop.close()

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
