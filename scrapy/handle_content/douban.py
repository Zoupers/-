#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 14:22
# @Author  : Ryu
# @Site    : 
# @File    : 爬虫-电影简介.py
# @Software: PyCharm
from scrapy.requests.g_handle import GUrlHandle
from scrapy.handle_db.DBApi import DbHandle
from bs4 import BeautifulSoup
import json


def get_urls():
    db = DbHandle()
    urls_list = db.get(table='movie', _range='id')
    urls = ['https://movie.douban.com/subject/%s/' % _id[0] for _id in urls_list]
    print(urls)
    request = GUrlHandle(content_handle=content_handle)
    request.get_contents(urls)


def content_handle(html):
    # html = get_more('more-actor')
    soup = BeautifulSoup(html,'lxml')
    # s1 = soup.find_all('div', {'id': 'info'})[0]
    try:
        content = soup.select('span[property="v:summary"]')[0].get_text().strip()
    except Exception as e:
        print('寻找简介', e)
        content = soup.select('span[class="all hidden"]')[0].get_text().strip()
    dic = soup.find_all('script', attrs={'type': "application/ld+json"})[0]
    # 不把换行符替换了的话，有些内容无法转化为字典
    dic = dic.getText().replace('\n', '')
    try:
        dic = json.loads(dic, encoding='utf-8')
    except Exception as e:
        print(e)
        print(dic)
    _id = dic['url'].split('/')[-2]
    del dic['@type'], dic['@context'], dic['description'], dic['aggregateRating']['@type']
    for director in dic['director']:
        del director['@type']
    for author in dic['author']:
        del author['@type']
    for actor in dic['actor']:
        del actor['@type']
    dic['describe'] = content
    final_dic = json.dumps(dic, ensure_ascii=False)
    print(final_dic)
    db = DbHandle()
    db.table = 'movie'
    db.execute('UPDATE `movie` SET `details`=%s where `id`=%s', (final_dic, _id))
    db.commit()



if __name__ == '__main__':
    get_urls()






