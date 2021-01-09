# -*- coding:utf-8 -*-
"""
    asyncio_requests.py
    ~~~~~~~~
    有现成的包, Requests + Gevent
    Ref: https://github.com/spyoungtech/grequests/blob/master/grequests.py

    :author: Fufu, 2021/1/9
"""
import grequests

from util import run_perf, gen_url


@run_perf
def main(worker):
    rs = [grequests.get(x) for x in gen_url(20)]
    for r in grequests.imap(rs, size=worker):
        r.encoding = 'utf-8'
        print(r.text)


if __name__ == '__main__':
    # 0.514683
    main(20)

    # 1.5983094
    # main(3)
