from scrapy.requests.g_handle import GUrlHandle
import re
import requests
from fake_useragent import UserAgent
from scrapy.handle_db.DBApi import DbHandle
import time


def get_base_connection():
    base_url = "https://movie.douban.com/top250?"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    film_connection = []
    for num in range(10):
        params = {
            "start": num * 25
        }
        response = requests.get(base_url, headers=headers, params=params)
        info = response.text
        connection = re.findall(r'<div class="hd">\s+<a href="(.+)" ', info)
        film_connection.extend(connection)
    get_every_connection(film_connection)


def get_every_connection(film_connection):
    base_url = "https://movie.douban.com{}"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    every_actor_connection = []
    for url in film_connection:
        response = requests.get(url, headers=headers)
        info = response.text
        actor_connection = re.findall(r'class="c.+s">\s*<h2>\s*.+\s*.+\s*.+\s*.\s*<a href="(.+)">', info)
        new_url = base_url.format(actor_connection[0])
        every_actor_connection.append(new_url)
    handle_actor_info(every_actor_connection)


def handle_actor_info(every_actor_connection):
    headers = {
        "User-Agent": UserAgent().chrome
    }
    all_actor_info_connection = []
    for url in every_actor_connection:
        response = requests.get(url, headers=headers)
        info = response.text
        some = re.findall('body.*?制片人', info, re.S)
        actor = re.findall(r'<li class="c.+y">\s*<a href="(.+)" t', some[0])
        all_actor_info_connection.extend(actor)
    actor_inner_info(all_actor_info_connection)


def actor_inner_info(all_actor_info_connection):
    headers = {
        "User-Agent": UserAgent().chrome
    }
    all_actor_information = []
    for url in all_actor_info_connection:
        response = requests.get(url, headers=headers)
        info = response.text


def get_urls():
    db = DbHandle(database='ranking')
    db.table = 'movie'
    actor_ids = db.get(_range='details')
    urls = []
    for ids in actor_ids:
        if ids[0]:
            id_list = re.findall('celebrity/(\\d*?)/', str(ids[0]))
            url_list = ['https://movie.douban.com/celebrity/%s/' % _id for _id in id_list]
            urls.extend(url_list)
        else:
            continue
    print(len(urls))
    request = GUrlHandle(content_handle=content_handle, max=400)
    request.get_contents(urls)


def content_handle(info):
    # all_actor_information = []
    name = re.findall(r'<div id="content">\s*<h1>(.+)</h1>', info)
    sex = re.findall(r'<span>性别<.+>:\s*(.*)\s*', info)
    constellation = re.findall(r'<span>星座<.+>:\s*(.*)\s*', info)
    birthday = re.findall(r'<span>出生日期<.+>:\s*(.*)\s*', info)
    birthplace = re.findall(r'<span>出生地<.+>:\s*(.*)\s*', info)
    professional = re.findall(r'<span>职业<.+>:\s*(.*)\s*', info)
    imdb_number = re.findall(r'<span>imdb编号<.+>:\s*.+>(.+)</a>', info)
    all_introduce = re.findall(r'<span class="all hidden">\s*(.+)<', info)
    if not all_introduce:
        normal_introduce = re.findall(r'<h2>\s*影人简介\s*.+\s*<.+>\s*</div>\s*<div class="bd">\s*(.+)\s*', info)
        _dict = {
            "姓名": name[0],
            "性别": sex[0],
            "星座": constellation[0],
            "出生日期": birthday[0],
            "出生地": birthplace[0],
            "职业": professional[0],
            "imdb编号": imdb_number[0],
            "简介": normal_introduce[0]
        }
        # all_actor_information.append(dict)
    else:
        _dict = {
            "姓名": name[0],
            "性别": sex[0],
            "星座": constellation[0],
            "出生日期": birthday[0],
            "出生地": birthplace[0],
            "职业": professional[0],
            "imdb编号": imdb_number[0],
            "简介": all_introduce[0]
        }
        # all_actor_information.append(dict)
    print(_dict)


if __name__ == '__main__':
    # get_base_connection()
    get_urls()
























