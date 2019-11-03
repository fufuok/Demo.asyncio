#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    process_mpool_ping.py
    ~~~~~~~~
    多进程, 进程池, Demo

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
import multiprocessing


def producer():
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        ips = f.read().strip().split('\n')
        return ips


def consumer(ip):
    """消费者, PING IP"""
    print('--- is consumer', ip)
    res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(ip))
    # print(ip, res)
    return ip, res


def main():
    """使用多进程进程池 multiprocessing.pool"""
    stime = time.perf_counter()

    ips = producer()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    # 全部完成后一起返回
    # for data in pool.map(consumer, ips):
    #     print(data)

    # 结果返回顺序与 ips 一致
    # for data in pool.imap(consumer, ips):
    #     print(data)

    # 先完成的先返回
    for data in pool.imap_unordered(consumer, ips):
        print(data)

    # tasks = [pool.apply_async(consumer, (ip,)) for ip in ips]
    # for task in tasks:
    #     res = task.get()
    #     print('res', res)

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
