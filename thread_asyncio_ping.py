#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    thread_asyncio_ping.py
    ~~~~~~~~
    线程和协程, 异步 IO
    协程里不能加入阻塞 IO, 如果一定要, 可以将其放入线程池
    推荐!

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor


def producer():
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        ips = f.read().strip().split('\n')
        return ips


def consumer(ip):
    """消费者, PING IP"""
    print('--- is consumer', ip, threading.currentThread(), flush=True)
    res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(ip))
    print(ip, res)

    return ip, res


def main():
    stime = time.perf_counter()

    max_worker = 3
    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor(max_worker)
    ips = producer()

    tasks = [loop.run_in_executor(pool, consumer, ip) for ip in ips]
    res = loop.run_until_complete(asyncio.wait(tasks))

    loop.close()
    print('result:', res)
    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
