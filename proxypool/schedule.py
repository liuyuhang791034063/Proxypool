# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       brain
   Description:      程序的大脑，控制整个代理池
   Author:           God
   date：            2018/8/10
-------------------------------------------------
   Change Activity:  2018/8/10
-------------------------------------------------
"""
__author__ = 'God'

import random
import asyncio
import aiohttp
from aiohttp import ClientProxyConnectionError
import time
from multiprocessing import Process

from db import Redis, RedisHttps
from setting import IP_MAX_NUM, IP_MIN_NUM, TEST_URL, DIE_TIME, POOL_TIME, TIME_OUT
from spider import SpiderManager


class GetIp(object):
    """
    通过爬虫get ip
    """
    def __init__(self):
        self._sp = SpiderManager()
        self._cp = CheckIp()

    def get_http_ip(self):
        """
        随机选择spider爬取ip
        :return:
        """
        check_sp_num = random.choice(range(self._sp.__SpiderCount__))
        proxies = self._sp.get_proxies(self._sp.__SpiderFunc__[check_sp_num])
        loop = asyncio.get_event_loop()
        tasks = [self._cp.check_http_proxy(proxy) for proxy in proxies]
        loop.run_until_complete(asyncio.wait(tasks))

    # def get_https_ip(self):
    #     """
    #     随机选择spider爬取ip
    #     :return:
    #     """
    #     check_sp_num = random.choice(range(self._sp.__SpiderCount__))
    #     proxies = self._sp.get_proxies(self._sp.__SpiderFunc__[check_sp_num])
    #     loop = asyncio.get_event_loop()
    #     tasks = [self._cp.check_https_proxy(proxy) for proxy in proxies]
    #     loop.run_until_complete(asyncio.wait(tasks))


class CheckIp(object):
    """
    负责检查ip
    """
    def __init__(self):
        self._sp = SpiderManager()
        self._db = Redis()
        self._db2 = RedisHttps()

    async def check_http_proxy(self, proxy):
        try:
            conn = aiohttp.TCPConnector(verify_ssl=True)
            async with aiohttp.ClientSession(connector=conn) as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(TEST_URL, proxy=real_proxy, timeout=TIME_OUT) as response:
                        if response.status == 200:
                            self._db.put(proxy)
                            print('Valid http proxy', proxy)
                        else:
                            print(response)
                except (ClientProxyConnectionError, TimeoutError, ValueError):
                    print('Invalid http proxy', proxy)
                    pass
        except Exception as e:
            pass

    async def check_https_proxy(self, proxy):
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'https://' + proxy
                    print('Testing', proxy)
                    async with session.get(TEST_URL, proxy=real_proxy, timeout=TIME_OUT) as response:
                        if response.status == 200:
                            self._db2.put(proxy)
                            print('Valid https proxy', proxy)
                        else:
                            print(response)
                except (ClientProxyConnectionError, TimeoutError, ValueError):
                    print('Invalid https proxy', proxy)
        except Exception as e:
            print(e)
            pass


class Schedule(object):
    def __init__(self):
        self._bi = GetIp()
        self._db = Redis()
        self._db2 = RedisHttps()

    @staticmethod
    def check_http_ip():
        sc = Schedule()
        while True:
            print("**********Start to check http proxies**********")
            if sc.check_number():
                sc._bi.get_http_ip()
            time.sleep(POOL_TIME)

    # @staticmethod
    # def check_https_ip():
    #     sc = Schedule()
    #     while True:
    #         print("**********Start to check https proxies**********")
    #         if sc.check_number2():
    #             sc._bi.get_https_ip()
    #         time.sleep(POOL_TIME)

    @staticmethod
    def kill_http_ip():
        sc = Schedule()
        while True:
            print("**********Start to kill http proxies**********")
            old_proxies = sc._db.get(int(sc._db.count*0.5))
            for old_proxy in old_proxies:
                print(old_proxy, "is be killed")
            print("**********End to kill http proxies**********")
            time.sleep(DIE_TIME)

    # @staticmethod
    # def die_ip2():
    #     sc = Schedule()
    #     while True:
    #         print("**********Start to die https proxies**********")
    #         sc._db2.get(int(sc._db2.count * 0.5))
    #         print("**********End to die https proxies**********")
    #         time.sleep(DIE_TIME)

    def check_number(self):
        """
        检查代理池大小
        :return:
        """
        number = self._db.count
        if number <= IP_MAX_NUM:
            return True
        elif number >= IP_MIN_NUM:
            self._db.get(int(self._db.count * 0.5))
        else:
            print("**********Too few proxies**********")
            time.sleep(5)

    # def check_number2(self):
    #     """
    #     检查代理池大小
    #     :return:
    #     """
    #     number = self._db2.count
    #     if number <= IP_MAX_NUM:
    #         return True
    #     else:
    #         self._db2.get(int(self._db2.count * 0.5))


class Run(object):
    def __init__(self):
        self._sd = Schedule()
        self.pool1 = Process(target=self._sd.check_http_ip)
        self.kill1 = Process(target=self._sd.kill_http_ip)

    def start(self):
        self.pool1.start()
        self.kill1.start()

    def shutdown(self):
        self.pool1.terminate()
        self.kill1.terminate()

    def get_proxy(self):
        return self._sd._db.get(1)

    def get_proxies_count(self):
        return self._sd._db.count
