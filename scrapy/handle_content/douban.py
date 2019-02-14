#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 14:22
# @Author  : Ryu
# @Site    : 
# @File    : 爬虫-电影简介.py
# @Software: PyCharm
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.handle_db.DBApi import DbHandle
import time
db = DbHandle()
# db.create_table('')


def get_html():
    args = {
        'subject':xxx#subject代号（网址）
    }
    args = urlencode(args)
    url = 'https://movie.douban.com/subject/?{}'.format(args)
    headers = {
    'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    request = Request(url,headers=headers)
    reponse = urlopen(request)
    html = reponse.read().decode()
    return html
# def get_dit(html):
#     soup = BeautifulSoup(html,'lxml')
#     s1 = soup.find_all('div',{'id':'info'})
#     text = []
#     for net in s1.select('span'):
#         con = net.get_text()
#         text = text.append(con)
#     return text
def get_actorsurl(html):
    # html = get_more('more-actor')
    soup = BeautifulSoup(html,'lxml')
    s1 = soup.find_all('div', {'id': 'info'})
    content = s1.select('span[class="all hidden"]').get_text()
    text = []
    for net in s1.select('span'):
        con = net.get_text()
        text = text.append(con)

    name = []
    author_url = []
    actors = []
    actor_url = []
    actors_url = []
    dic = soup.find_all('script', {'type="application/ld+json"'})
    director = dic['director']

    director_url = director['url']
    director = director['name']
    actors_url.append(director_url)

    author = dic['author']
    for auth in author:
        auth = auth['name']
        name.append(auth)
        auth_url = auth['url']
        _url = 'http://movie.douban.com/?{}'.format(auth_url)
        author_url.append(_url)
    actors_url += author_url
    actor = dic['actor']
    for act in actor:
        act = act['name']
        actors.append(act)
        act_url = act['url']
        __url = 'http://movie.douban.com/?{}'.format(act_url)
        actor_url.append(__url)
    actors_url += actor_url
    final = {
        'director':director,
        'author':name,
        'actor':actors,
        'dit':text,
        'short': content,
        'actors_url':actors_url
        #'actors_url': [{'director_url':director_url,'auth_url':author_url,'actors_url':actor_url}]
    }
    db.save(final, table='')
    # return actor_url

def handle_html():
    dit = get_dir(html)







