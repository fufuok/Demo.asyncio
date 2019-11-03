#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    process_queue_ping.py
    ~~~~~~~~
    多进程, 队列, Demo
    全局变量无法在多进程中使用
    普通的 Queue 不能用于进程间通信, multiprocessing.Queue() 不能用于 pool, 需要用 Manager.Queue()
    Pipe 只能用于 2 个进程间通信(简化版 Queue), 性能比 Queue 高

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
import multiprocessing


def producer(q, pool):
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        for ip in f:
            ip = ip.strip()
            if ip:
                q.put(ip)
                print('+++ producer put', ip)
                pool.apply_async(consumer, (q,))


def consumer(q):
    """消费者, PING IP"""
    ip = q.get()
    print('--- consumer get', ip)
    res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(ip))
    q.task_done()
    print(ip, res)


def main():
    stime = time.perf_counter()

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    q = multiprocessing.Manager().Queue()

    producer(q, pool)

    pool.close()
    pool.join()

    print('the end: {}s'.format(time.perf_counter() - stime))


def pipe_producer(s):
    """生产者, 获取待 PING IP"""
    s.send('8.8.8.8')


def pipe_consumer(r):
    """消费者, PING IP"""
    ip = r.recv()
    print('--- consumer recv', ip)
    res = subprocess.getoutput('ping {} -i 0.1 -c 5 -w 3 | tail -1'.format(ip))
    print(ip, res)


def main_pipe():
    recv_pipe, send_pipe = multiprocessing.Pipe()
    my_producer = multiprocessing.Process(target=pipe_producer, args=(send_pipe,))
    my_consumer = multiprocessing.Process(target=pipe_consumer, args=(recv_pipe,))
    my_producer.start()
    my_consumer.start()
    my_producer.join()
    my_consumer.join()


if __name__ == '__main__':
    # main()
    main_pipe()
