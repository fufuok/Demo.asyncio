#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    process_share.py
    ~~~~~~~~
    多进程, 共享内存, Demo

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
import multiprocessing


def producer(share):
    """生产者, 获取待 PING IP"""
    with open('ip.txt', 'r') as f:
        share.append(f.read().strip().split('\n'))


def consumer(share):
    """消费者, PING IP"""
    print('consumer', share)


def main():
    stime = time.perf_counter()

    # process_Value = multiprocessing.Manager().Value()
    share_list = multiprocessing.Manager().list()
    my_producer = multiprocessing.Process(target=producer, args=(share_list,))
    my_consumer = multiprocessing.Process(target=consumer, args=(share_list,))
    my_producer.start()
    my_consumer.start()
    my_producer.join()
    my_consumer.join()

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
