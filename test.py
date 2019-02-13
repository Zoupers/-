# this is used to test each function
import re
from fake_useragent import UserAgent
from scrapy.requests.request_handle import AsyncGet, get_content
import time
import requests
from scrapy.handle_db.DBApi import DbHandle
db = DbHandle()
t = time.time()
fake = UserAgent


def get_proxies():
    http = requests.get('http://127.0.0.1:8080/get/http').text
    https = requests.get('http://127.0.0.1:8080/get/https').text
    # print({'http': 'http://'+http, 'https': 'https://'+https})
    return https.split(':')[0]


def main():
    urls_ = db.get(table='init')[0][1]
    import json
    urls = json.loads(urls_)
    tx = AsyncGet(urls, x_forwarded_for='27.23.252.35')
    for i in tx.get_content:
        print(i)
        u = re.findall('<a href="(https://movie.douban.com/subject/.*?)"', i)
        for z in u:
            print(z)
        tt = AsyncGet(u, x_forwarded_for=get_proxies())
        print(len(tt.get_content))
    t1 = AsyncGet(urls, x_forwarded_for='175.148.77.188')
    print(t1.get_content)
    t2 = AsyncGet(urls, x_forwarded_for='218.26.227.108')
    print(t2.get_content)
    print(time.time() - t)


if __name__ == '__main__':
    main()