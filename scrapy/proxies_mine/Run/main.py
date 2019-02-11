# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main.py  
   Description :  运行主函数
   Author :       JHao
   date：          2017/4/1
-------------------------------------------------
   Change Activity:
                   2017/4/1: 
-------------------------------------------------
"""
# __author__ = 'JHao'

import sys
from multiprocessing import Process

sys.path.append('.')
sys.path.append('..')
# from Api.ProxyApi import run as ProxyApiRun
from scrapy.proxies_mine.Schedule.ProxyValidSchedule import run as ValidRun
from scrapy.proxies_mine.Schedule.ProxyRefreshSchedule import run as RefreshRun


def run():
    p_list = list()
    # 可以根据需要启动flask网站
    # p1 = Process(target=ProxyApiRun, name='ProxyApiRun')
    # p_list.append(p1)
    p2_http = Process(target=ValidRun, name='ValidRun_http', args=('http',))
    p_list.append(p2_http)
    p2_https = Process(target=ValidRun, name='ValidRun_https', args=('https',))
    p_list.append(p2_https)
    p3_http = Process(target=RefreshRun, name='RefreshRun_http', args=('http',))
    p_list.append(p3_http)
    p3_https = Process(target=RefreshRun, name='RefreshRun_https', args=('https',))
    p_list.append(p3_https)

    for p in p_list:
        p.daemon = True
        p.start()
    # for p in p_list:
    #     p.join()


if __name__ == '__main__':
    run()
