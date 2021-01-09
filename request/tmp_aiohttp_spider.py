#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    tmp_aiohttp_spider.py
    ~~~~~~~~
    代码来源于下面链接:
    asyncio 爬虫, 去重, 入库(使用异步的方式 aiomysql, pymysql 已经不适用了)
    Ref: https://blog.csdn.net/hubingshabi/article/details/101074244

    :author: Fufu, 2021/1/9
"""
import asyncio
import re

import aiohttp
import aiomysql
from pyquery import PyQuery

stopping = False
start_url = 'https://cuiqingcai.com/'
waiting_urls = []
seen_urls = set()


async def article_handler(url, session, pool):
    """
    function:提取页面title的信息，且将页面中出现的url地址加入waiting_url列表中
    :param url:
    :param session:
    :param pool:
    :return:
    """
    print('start get url: {}'.format(url))
    # 获取文章详情，并解析入库
    html = await fetch(url, session)
    # 最终要提取的url地址，添加到seen_urls列表中
    seen_urls.add(url)
    # extract_urls提取出页面中所有的url，解析是通过cpu完成的，不会耗费io的
    extract_urls(html)

    # 获取页面信息对象
    pq = PyQuery(html)
    title = pq('title').text()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # await cur.execute("SELECT 42;")
            insert_sql = "insert into article_test(title) values('{}') ".format(title)
            await cur.execute(insert_sql)

    # pool.close()
    # await pool.wait_closed()


async def consumer(pool):
    """
    function
    :param pool:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        while not stopping:
            if len(waiting_urls) == 0:
                await asyncio.sleep(0.5)
                continue
            url = waiting_urls.pop()

            # print('start get url: {}'.format(url))
            # 过滤url地址，相匹配的且没循环过的url
            if re.match('https://cuiqingcai.com/\d+.html', url):
                if url not in seen_urls:
                    asyncio.ensure_future(article_handler(url, session, pool))
                    await asyncio.sleep(0.5)
            # else:
            #     if url not in seen_urls:
            #         asyncio.ensure_future(init_urls(url,session))


# 获取请求的start_url中的所有url，网络请求比较费io
async def init_urls(url, session):
    html = await fetch(start_url, session)
    seen_urls.add(url)
    extract_urls(html)


# 读取单个url信息

async def fetch(url, session):
    """
    function：读取单个url地址页面信息
    :param url:
    :param session:
    :return: 返回页面信息
    """
    try:
        async with session.get(url) as resp:
            if resp.status in [200, 201]:
                html = await resp.text()
                return html
                # print(data)
    except Exception as e:
        print(e)


# PyQuery解析出所有的url，解析是通过cpu完成的，不会耗费io的
def extract_urls(html):
    """
    function:提取所有url地址，并添加到waiting_urls等待列表中
    :param html:
    :return: None
    """
    # urls = []
    pq = PyQuery(html)
    # print('PyQuery',pq)

    for link in pq.items('a'):
        url = link.attr('href')
        if url and url.startswith('https') and url not in seen_urls:
            # print('url:{}'.format(url))
            # urls.append(url)
            waiting_urls.append(url)


async def main(loop):
    # 等待mysql连接建立好
    """autocommit=True, charset='utf8'不设置的话，数据库会没数据"""
    # global pool
    # 1.建立异步连接池
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='root',
                                      db='aiomysql_test', loop=loop, autocommit=True, charset='utf8')

    async with aiohttp.ClientSession() as session:
        # 2.返回初始页面信息
        html = await fetch(start_url, session)
        # 3. 添加初始url地址
        seen_urls.add(start_url)
        # 4. 提取页面信息，获取页面中所有url地址
        extract_urls(html)

    # 将consumer注册到事件循环中
    asyncio.ensure_future(consumer(pool))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(main(loop))
    loop.run_forever()
