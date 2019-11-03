#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    process_ping.py
    ~~~~~~~~
    多进程 Demo

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
    stime = time.perf_counter()

    processs = []
    for ip in producer():
        t = multiprocessing.Process(target=consumer, args=(ip,))
        processs.append(t)
    for t in processs:
        t.start()
        print('进程ID', t.pid)
    for t in processs:
        t.join()

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
