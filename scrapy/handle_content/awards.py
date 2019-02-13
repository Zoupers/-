import requests
from scrapy.handle_db.DBApi import DbHandle
from scrapy.requests.request_handle import get_content
from lxml import etree

db = DbHandle()


url = 'https://movie.douban.com/subject/1292052/awards/'


def get_awards(url):
    sessions = requests.session()
    sessions.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    r = sessions.get(url)
    r.encoding = 'utf-8'
    text = r.text
    awards_handle(text)


def get_url():
    l = db.get(table='movie', _range='(`id`, `awards_url`)')
    for i in l:
        get_content(i[0], hook=awards_handle)


def awards_handle(text):
    content = etree.HTML(text)
    d = content.xpath("//div[@class='awards']")
    num = len(d)
    data_list = []
    for n in range(num):
        d1 = d[n].xpath('string(.)').split()
        data = {
            '获奖名字' : d1[0:2],
            '获奖内容' : d1[2:]
        }
        data_list.append(data)
    # save_awards(movie_id, data)


def save_awards(movie_id, data):
    db.updata(table='movie',id=movie_id, data=data)
get_awards(url)
