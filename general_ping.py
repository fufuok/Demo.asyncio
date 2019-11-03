#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    general_ping.py
    ~~~~~~~~
    同步方式 Demo

    :author: Fufu, 2019/11/3
"""
import time
import subprocess


def producer():
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        ips = f.read().strip().split('\n')
        return ips


def consumer(ip):
    """消费者, PING IP"""
    print('--- is consumer', ip)
    res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(ip))
    return res


def main():
    stime = time.perf_counter()

    for ip in producer():
        res = consumer(ip)
        print(ip, res)

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
