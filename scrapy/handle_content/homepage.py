#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from scrapy.handle_db.DBApi import DbHandle
from scrapy.requests.request_handle import get_content
import re
from bs4 import BeautifulSoup


db = DbHandle(database='ranking')
db.create_table('')
#url = "https://movie.douban.com/top250?start=200&filter="
a=[]


def get_url():
    url_list = db.get(table='init_url', _range=('name', 'url'))
    for url in url_list:
        get_content(url=url, hook=handle_content)


def get_content(url):
    r = requests.get(url)
    demo = r.text


def handle_content(demo):
    soup = BeautifulSoup(demo, 'html.parser')
    ol = soup.find('ol', class_='grid_view')
    #text = ol.prettify()
    for i in ol.find_all('li'):
        movie_name = i.find('span', attrs={'class': 'title'}).get_text()       #名字
        rank = i.find('span', attrs={'class': 'rating_num'}).get_text()     #分数
        star = i.find('div', attrs={'class': 'star'})
        star_num = star.find(text=re.compile('评价'))     #评价人数
        info = i.find('p', attrs={'class':''}).get_text() #基本信息
        info = info.strip().replace(' ','')

        info_one = info.split()     #弄出导演主演年份
        director = info_one[0]
        main_actors = info_one[1]
        year = info_one[2]

        info_two = info.replace('/','').split() #弄出地区和类型
        try:
            class_ = info_two[4]
            countries = info_two[3]
        except IndexError:
            class_ = info_two[3]
            countries = info_two[2]

        id = i.a['href']
        id = id.replace('https://movie.douban.com/subject/','')
        id = id.replace('/','')
        #print(id)

        review = i.find('span', attrs={'class': 'inq'})     #判断是否有短评
        if review:
            review = review.get_text()
        else:
            review = 'none review'


        content = {"movie_name" : movie_name,
                   "rank" : rank,
                   "star_num" : star_num,
                   "id":id,
                   "director" : director,
                   "main_actors" : main_actors,
                   "year" : year,
                   "countries" : countries,
                   "class" : class_,
                   "review" : review
        }
        db.save(table='brife_movie', data=content)
        # a.append(content)
        print(a)



def geturl(n):
    url = 'https://movie.douban.com/top250?start='+str(25*n)+'&filter='

    return url

if __name__ == '__main__':
    for n in range(0,10):
        url = geturl(n)
        get_content(url)
