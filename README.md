# Python 并发, 并行, 协程和异步IO, 示例代码

## 功能

1. 多线程(函数和类)
2. 多线程 + 线程池
3. 多线程队列
4. 多线程并发数控制
5. 多进程
6. 多进程 + 进程池 1, 2
7. 多进程队列 1, 2
8. 多进程内存共享
9. asyncio
10. asyncio + ThreadPoolExecutor
11. asyncio + aioping
12. asyncio.subprocess
13. asyncio + 阻塞 secket
14. asyncio + 非阻塞 secket
15. asyncio + requests + ThreadPoolExecutor
16. grequests(requests + gevent)
17. asyncio + aiohttp + Semaphore
18. [request] (目录中包含 https 的并发请求示例, 基于 asyncio)

## 注意

代码中 `pool` `loop` 等在实际使用结束时请调用 `shutdown()` 或 `close()` 等方法主动释放资源. 

在不复用 `pool` 的场景, 常用做法是使用 `with ... as pool:` 来避免显式调用结束指令.

## 说明

示例代码基于 Python3.6+, 但 Python3.9+ 新增的一些特性就可能没有演示了.

近期有个大量 PING IP 的事务, 适合并发执行, 之前 [Demo.shell](https://github.com/fufuok/Demo.shell) 里有 Shell 方案.

顺便写些 Python 中各类并发代码, 备忘.
