#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    tmp_queue.py
    ~~~~~~~~

    :author: Fufu, 2019/11/3
"""
import queue
import threading


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print(item)
        q.task_done()


def source():
    return range(10)


q = queue.Queue()
threads = []
num_worker_threads = 2
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in source():
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()
