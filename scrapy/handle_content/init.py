# the scrapy project start urls

from scrapy.requests.g_handle import GUrlHandle
from scrapy.handle_db.DBApi import DbHandle
import re


def db_save(name, data):
    db = DbHandle()
    db.table = 'init'
    data_ = [name, data]
    try:
        db.save(data_)
    except Exception as e:
        print(e)



def top250():
    i_url = 'https://movie.douban.com/top250'
    urls = []
    add = '?start=%s&filter='
    for i in range(10):
        if i == 0:
            urls.append(i_url)
            continue
        url = i_url + add % (25*i)
        urls.append(url)
    db_save('top250', str(urls))


# def classify_content_handle(content):
#     pass


def classify():
    i_url = 'https://movie.douban.com/chart'
    session = GUrlHandle(content_handle=None)
    context = session.get_content(i_url)
    block = re.findall('id="content".*?(class="types".*?</div>)', context, re.S)[0]
    pre_urls = re.findall('href=".*?type_name=(.*?).*?type=(.*?)"', block, re.S)
    for pre in pre_urls:
        url = f'https://movie.douban.com/j/chart/top_list?type={pre[1]}&interval_id=100%3A90&action=&start=20&limit=250'
        name = pre[0]
        db_save(name, url)


def new_content_handle():
    pass


def new():
    db_save('new', 'https://movie.douban.com/chart')


def box_office():
    import time
    import requests
    # 注意，这里要加上host参数，而且返回来的不一定带有票房信息，要甄别
    while True:
        print(requests.get('http://dianying.nuomi.com/movie/boxrefresh', headers={'Host': 'dianying.nuomi.com',
                                                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}).text)
        time.sleep(3)


def main():
    top250()
    classify()
    new()


if __name__ == '__main__':
    # session = GUrlHandle()
    pass
