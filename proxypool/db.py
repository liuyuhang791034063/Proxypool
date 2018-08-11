# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       db
   Description:
   Author:           God
   date：            2018/8/9
-------------------------------------------------
   Change Activity:  2018/8/9
-------------------------------------------------
"""
__author__ = 'God'

import redis
from setting import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB2


class Redis(object):
    def __init__(self):
        if REDIS_PASSWORD is None:
            self._db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        else:
            self._db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

    def get(self, count=1):
        """
        get proxies from redis
        :return:
        """
        proxies = self._db.lrange("proxies", 0, count-1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        self._db.rpush("proxies", proxy)

    @property
    def count(self):
        return self._db.llen("proxies")


class RedisHttps(object):
    def __init__(self):
        if REDIS_PASSWORD is None:
            self._db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB2)
        else:
            self._db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB2, password=REDIS_PASSWORD)

    def get(self, count=1):
        """
        get proxies from redis
        :return:
        """
        proxies = self._db.lrange("proxies", 0, count-1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        self._db.rpush("proxies", proxy)

    @property
    def count(self):
        return self._db.llen("proxies")