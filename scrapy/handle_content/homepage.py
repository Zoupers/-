#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from scrapy.requests.g_handle import GUrlHandle
from scrapy.handle_db.DBApi import DbHandle
import re
import json
from bs4 import BeautifulSoup


def table_create(database=None):
    # db = pymysql.connect(host='localhost', user='root', password='131421', database='ranking')
    db = DbHandle(database='ranking')
    # cursor = db.cursor()
    sql = '''CREATE TABLE `movie`(
        `movie_name` CHAR(30) NOT NULL ,
        `rank` FLOAT,
        `star_num` VARCHAR(15),
        `director` VARCHAR(100),
        `main_actors` VARCHAR(50),
        `year` VARCHAR(200) ,
        `class` VARCHAR(20),
        `countries` VARCHAR(20),
        `id` CHAR(15) PRIMARY KEY NOT NULL ,
        `review` TEXT,
        `details` TEXT
        )'''
    try:
        db.execute(query=sql)
    except Exception as e:
        print(e)


def get_url():
    table_create()
    db = DbHandle(database='ranking')
    request = GUrlHandle(content_handle=content_handle)
    url_list = db.get(table='init', _range='name, urls')
    for i in url_list:
        urls = json.loads(i[1])
        print(urls)
        request.get_contents(urls)


def content_handle(demo):
    # db = pymysql.connect(host='localhost', user='root', password='131421', database='ranking')
    # cursor = db.cursor()
    db = DbHandle()
    db.table = 'movie'
    soup = BeautifulSoup(demo, 'html.parser')
    ol = soup.find('ol', class_='grid_view')
    for i in ol.find_all('li'):
        data = []
        movie_name = i.find('span', attrs={'class': 'title'}).get_text()#名字
        data.append(movie_name)
        rank = i.find('span', attrs={'class': 'rating_num'}).get_text()     #分数
        data.append(rank)
        star = i.find('div', attrs={'class': 'star'})
        star_num = star.find(text=re.compile('评价'))     #评价人数
        data.append(star_num)
        info = i.find('p', attrs={'class':''}).get_text() #基本信息
        info = info.strip().replace(' ','')

        info_one = info.split()     #弄出导演主演年份
        director = info_one[0]
        data.append(director)
        main_actors = info_one[1]
        data.append(main_actors)
        year = info_one[2]
        data.append(year)

        info_two = info.replace('/','').split() #弄出地区和类型
        try:
            class_ = info_two[4]
            countries = info_two[3]
        except IndexError:
            class_ = info_two[3]
            countries = info_two[2]
        data.append(class_)
        data.append(countries)
        _id = i.a['href']
        _id = _id.replace('https://movie.douban.com/subject/','')
        _id = _id.replace('/','')
        data.append(_id)

        review = i.find('span', attrs={'class': 'inq'})     #判断是否有短评
        if review:
            review = review.get_text()
        else:
            review = 'none review'
        data.append(review)
        # print(data)
        if db.execute('SELECT * FROM `movie` where id=%s', (_id, )) == 0:
            db.save(data,_range='movie_name,rank,star_num,director,main_actors,year,class,countries,id,review')


if __name__ == '__main__':
    # for n in range(0,10):
    #     url = geturl(n)
    #     get_content(url)
    get_url()
