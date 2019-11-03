#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    thread_queue_ping.py
    ~~~~~~~~
    多线程, 队列, Demo

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
import threading
import queue


def producer(q):
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        for ip in f:
            ip = ip.strip()
            if ip:
                q.put(ip)
                print('+++ is producer', ip)
                # time.sleep(1)


def consumer(q):
    """消费者, PING IP"""
    while True:
        ip = q.get()
        # if ip is None:
        #     break
        print('--- is consumer', ip)
        res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(ip))
        q.task_done()
        print(ip, res)
        # time.sleep(10)


def main():
    stime = time.perf_counter()

    max_workers = 3
    q = queue.Queue()

    threads = []
    for i in range(max_workers):
        t = threading.Thread(target=consumer, args=(q,))
        t.setDaemon(True)
        t.start()
        threads.append(t)

    producer(q)

    # 等待所有任务完成
    q.join()

    # 结束线程
    # for i in range(max_workers):
    #     q.put(None)
    # for t in threads:
    #     t.join()

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
