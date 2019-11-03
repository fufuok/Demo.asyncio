#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    asyncio_ping.py
    ~~~~~~~~
    协程, 异步 IO
    推荐!!!

    :author: Fufu, 2019/11/3
"""
import threading
import time
import asyncio


def producer():
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        ips = f.read().strip().split('\n')
        return ips


async def consumer(ip):
    """消费者, PING IP"""
    print('--- is consumer', ip, threading.currentThread(), flush=True)

    cmd = 'ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(ip)
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    # 等待该子进程运行结束
    stdout, stderr = await process.communicate()

    # 运行结果
    res = stdout.decode().strip()
    print('res:' if process.returncode == 0 else 'failed:', ip, res, flush=True)

    return ip, res


def mk_chunks(datas, chunk_size=30):
    """数据分片(控制并发数)"""
    for i in range(0, len(datas), chunk_size):
        yield datas[i:chunk_size + i]


def main():
    stime = time.perf_counter()

    max_worker = 3
    ips = producer()
    loop = asyncio.get_event_loop()

    results = []
    tasks = [asyncio.ensure_future(consumer(ip)) for ip in ips]
    for task_chunks in mk_chunks(tasks, max_worker):
        res = loop.run_until_complete(asyncio.gather(*task_chunks))
        results += res

    loop.close()

    print('result:', results)
    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
