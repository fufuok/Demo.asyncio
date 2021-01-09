# -*- coding:utf-8 -*-
"""
    util.py
    ~~~~~~~~
    Ref: https://www.jianshu.com/p/eed5da9965f2

    :author: Fufu, 2021/1/9
"""
import asyncio
import socket
import ssl
import time
from functools import wraps


def gen_url(n, url=True):
    """生成测试网址"""
    for i in range(n):
        yield f'https://cs.xunyou.com/gd.html?{i}' if url else ('cs.xunyou.com', f'/gd.html?{i}')


async def async_get_url(host, path='/', port=443):
    """使用 socket 请求 url (非阻塞 IO)"""

    # 建立 socket 连接
    reader, writer = await asyncio.open_connection(host, port, ssl=port == 443)

    # 发送请求
    writer.write(f'GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n'.encode('utf-8'))

    # 这是一个与底层 IO 输入缓冲区交互的流量控制方法
    # 当缓冲区达到上限时, drain() 阻塞, 待到缓冲区回落到下限时, 写操作恢复
    # 当不需要等待时, drain() 会立即返回, 例如上面的消息内容较少, 不会阻塞
    # 这就是一个控制消息的数据量的控制阀
    await writer.drain()

    # 接收数据
    resp = b''
    # while True:
    #     # 读取数据是阻塞操作, 释放 CPU
    #     line = await reader.readline()
    #     if line:
    #         resp += line
    #     else:
    #         break
    async for b in reader:
        resp += b

    writer.close()

    try:
        return resp.decode('utf-8')
    except Exception as e:
        return f'{host} response decoding failure'


def get_url(host, path='/', port=443):
    """使用 socket 请求 url (阻塞 IO)"""

    # 建立 socket 连接
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))

    # SSL
    if port == 443:
        conn = ssl.wrap_socket(conn)

    # 发送请求
    conn.send(f'GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n'.encode('utf-8'))

    # 接收数据
    resp = b''
    while True:
        b = conn.recv(1024)
        if b:
            resp += b
        else:
            break

    conn.close()

    try:
        return resp.decode('utf-8').split('\r\n\r\n', 1)[1]
    except Exception as e:
        return f'{host} response decoding failure'


def run_perf(fn):
    """时间消耗统计"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = fn(*args, **kwargs)
        end = time.perf_counter()
        print('\n~~~~~~\n{}.{} : {}\n~~~~~~\n'.format(fn.__module__, fn.__name__, end - start))
        return res

    return wrapper
