# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       utils
   Description:      封装request
   Author:           God
   date：            2018/8/9
-------------------------------------------------
   Change Activity:  2018/8/9
-------------------------------------------------
"""
__author__ = 'God'

import requests
from fake_useragent import UserAgent, FakeUserAgentError
from requests.exceptions import ConnectionError


def get_html(url, options={}):
    try:
        agent = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent': agent.__getattr__('random'),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers, **options)
    print('Getting', url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('获取源码失败')
            return
    except ConnectionError:
        print('连接失败')

