# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       spider
   Description:
   Author:           God
   date：            2018/8/9
-------------------------------------------------
   Change Activity:  2018/8/9
-------------------------------------------------
"""
__author__ = 'God'

from bs4 import BeautifulSoup
import json
import time
import re

from utils import get_html


class SpiderMetaclass(type):
    """
    定义爬虫的元类，用于动态加载爬虫类中的各种代理网的爬取方法
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__SpiderFunc__'] = []
        for key, value in attrs.items():
            if 'spider_' in key:
                attrs['__SpiderFunc__'].append(key)
                count += 1
        attrs['__SpiderCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class SpiderManager(object, metaclass=SpiderMetaclass):
    """
    爬虫管理
    """
    def get_proxies(self, callback):
        proxies = []
        print('Spider', callback)
        for proxy in eval('self.{}()'.format(callback)):
            if proxy:
                print('From', callback, 'getting', proxy)
                proxies.append(proxy)
            else:
                print('Failed to get proxy,continue next')
        return proxies

    def spider_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_html(start_url)
        results = json.loads(html).get('RESULT')
        for proxy in results:
            ip = proxy.get('ip')
            port = proxy.get('port')
            yield '{0}:{1}'.format(ip, port)

    def spider_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
            soup = BeautifulSoup(get_html(start_url), 'lxml')
            ips = soup.find_all('td', attrs={'data-title': 'IP'})
            ports = soup.find_all('td', attrs={'data-title': 'PORT'})
            for j in range(len(ips)):
                yield '{0}:{1}'.format(ips[j].text, ports[j].text)
            time.sleep(1)

    def spider_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/wt/{}'.format(i)
            ip_port = re.compile('<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            re_ip_port = re.findall(ip_port, get_html(start_url,))
            for ip, port in re_ip_port:
                ip.replace(' ', '')
                port.replace(' ', '')
                yield '{0}:{1}'.format(ip, port)

    def spider_66ip(self):
        for i in range(1, 5):
            start_url = 'http://www.66ip.cn/{}.html'.format(i)
            ip_port = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            re_ip_port = re.findall(ip_port, get_html(start_url))
            for ip, port in re_ip_port[1:]:
                ip.replace(' ', '')
                port.replace(' ', '')
                yield '{0}:{1}'.format(ip, port)

    # def spider_data5u(self):
    #     for i in ['gngn', 'gnpt']:
    #         start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
    #         ips_ports = BeautifulSoup(get_html(start_url), 'lxml').find_all('ul', class_='l2')
    #         for ip_port in ips_ports:
    #             ip = ip_port.find_all('span')[0].text.replace(' ', '')
    #             port = ip_port.find_all('span')[1].text.replace(' ', '')
    #             yield '{0}:{1}'.format(ip, port)


if __name__ == '__main__':
    a = SpiderManager()
    a.get_proxies('spider_data5u')
