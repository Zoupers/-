import requests
from lxml import etree

url = 'https://movie.douban.com/subject/1292052/awards/'
def get_awards(url):
    sessions = requests.session()
    sessions.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    r = sessions.get(url)
    r.encoding = 'utf-8'
    text = r.text
    awards_handle(text)


def get_url():
    pass


def awards_handle(text):
    content = etree.HTML(text)
    d = content.xpath("//div[@class='awards']")
    num = len(d)
    for n in range(num):
        d1 = d[n].xpath('string(.)').split()
        data = {
            '获奖名字' : d1[0:2],
            '获奖内容' : d1[2:]
        }
        save_awards(movie_id, data)


def save_awards(movie_id, data):
    pass
get_awards(url)
