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
IP_MIN_NUM = 20  # 代理最小
TEST_URL = 'http://icanhazip.com/'  # 代理测试Url

# 时间配置
DIE_TIME = 120  # 杀掉一半代理间隔时间
POOL_TIME = 10  # 爬虫爬取代理间隔时间
TIME_OUT = 5   # 代理测试超时等待时间
