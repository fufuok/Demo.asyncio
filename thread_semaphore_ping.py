#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    thread_semaphore_ping.py
    ~~~~~~~~
    多线程(类), 并发数量控制(进入某段代码的线程数), Demo

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
import threading


class Producer(threading.Thread):
    """生产者, 获取待 PING IP, 并开启消费者线程"""

    def __init__(self, sem):
        self.sem = sem
        super().__init__()

    def run(self):
        with open('ip.txt', 'r') as f:
            for ip in f:
                ip = ip.strip()
                if ip:
                    self.sem.acquire()
                    print('--- is producer')
                    t = Consumer(ip, self.sem)
                    t.start()


class Consumer(threading.Thread):
    """消费者, PING IP"""

    def __init__(self, ip, sem):
        self.ip = ip
        self.sem = sem
        super().__init__()

    def run(self):
        print('--- is consumer', self.ip)
        res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(self.ip))
        print(self.ip, res)
        self.sem.release()


def main():
    # stime = time.perf_counter()

    max_workers = 3
    sem = threading.Semaphore(max_workers)
    producer = Producer(sem)
    producer.start()

    # print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
