# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       setting
   Description:
   Author:           God
   date：            2018/8/9
-------------------------------------------------
   Change Activity:  2018/8/9
-------------------------------------------------
"""
__author__ = 'God'


# Redis 配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 4
REDIS_DB2 = 5
# 如果没有设置密码 REDIS_PASSWORD=None
REDIS_PASSWORD = '123456'

# 调度配置
IP_MAX_NUM = 100
IP_MIN_NUM = 20
TEST_URL = 'http://icanhazip.com/'

DIE_TIME = 120
POOL_TIME = 10
TIME_OUT = 5
