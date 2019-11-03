#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    thread_cls_ping.py
    ~~~~~~~~
    多线程(类) Demo

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
import threading


def producer():
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        ips = f.read().strip().split('\n')
        return ips


class Consumer(threading.Thread):
    """消费者, PING IP"""

    def __init__(self, ip):
        self.ip = ip
        super().__init__()

    def run(self):
        print('--- is consumer', self.ip)
        res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(self.ip))
        print(self.ip, res)


def main():
    stime = time.perf_counter()

    threads = []
    for ip in producer():
        t = Consumer(ip)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
