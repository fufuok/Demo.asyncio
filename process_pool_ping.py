#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    process_pool_ping.py
    ~~~~~~~~
    多进程, 进程池, Demo
    多进程能利用多个 CPU, 多线程只能使用一个 CPU
    进程切换代价比线程大
    CPU 计算优先多进程, IO 编程优先多线程
    进程可以 os.fork(), 会将 fork 后的内容完整拷贝并独立运行

    :author: Fufu, 2019/11/3
"""
import time
import subprocess
from concurrent import futures


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

    ips = producer()

    with futures.ProcessPoolExecutor(3) as pool:
        tasks = [pool.submit(consumer, (ip)) for ip in ips]
        for future in futures.as_completed(tasks):
            ip, res = future.result()
            print('res: ', ip, res)

    # pool = futures.ProcessPoolExecutor(max_workers=3)

    # 非阻塞, submit 函数提交要执行的函数到线程池
    # task1 = pool.submit(consumer, (ips[0]))

    # tasks = [pool.submit(consumer, (ip)) for ip in ips]
    # 主线程等待任务全部完成或第一个完成时继续执行
    # futures.wait(tasks)
    # futures.wait(tasks, return_when=futures.FIRST_COMPLETED)
    #
    # 每当有任务完成时获取其返回值
    # for future in futures.as_completed(tasks):
    #     ip, res = future.result()
    #     print('res: ', ip, res)

    # 直接使用 pool.map 获取完成时的 task 返回值(不用手动 submit, 且返回顺序与 ips 顺序相同)
    # for data in pool.map(consumer, ips):
    #     print('res: ', data)
    #
    # 可使用 with
    # with futures.ProcessPoolExecutor(3) as pool:
    #     for data in pool.map(consumer, ips):
    #         print('res: ', data)

    # 其他方法
    # print(task1.done())
    # print(task1.cancel())
    # time.sleep(3)
    # print(task1.done())
    #
    # 获取 task 的执行结果
    # print(task1.result())

    print('the end: {}s'.format(time.perf_counter() - stime))


if __name__ == '__main__':
    main()
