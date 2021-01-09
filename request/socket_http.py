# -*- coding:utf-8 -*-
"""
    socket_http.py
    ~~~~~~~~
    socket 原生请求, 阻塞 IO

    :author: Fufu, 2021/1/9
"""
from util import run_perf, get_url, gen_url


@run_perf
def main():
    for url in gen_url(20, False):
        html = get_url(*url)
        print('...' * 100, html)


if __name__ == '__main__':
    # 4.3785628
    main()
