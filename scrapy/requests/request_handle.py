# handle url and content get request

import requests
from fake_useragent import UserAgent
import time
t = time.time()
fake = UserAgent()


def get_proxies():
    http = requests.get('http://127.0.0.1:8080/get/http').text
    https = requests.get('http://127.0.0.1:8080/get/https').text
    # print({'http': 'http://'+http, 'https': 'https://'+https})
    return {'http': 'http://'+http, 'https': 'https://'+https}


# class Request(object):
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)

#     def get_content(self, url):
#         pass


def get_content(url):
    headers = {'User-Agent': fake.random}
    proxies = get_proxies()
    req = requests.get(url, headers=headers, proxies=proxies)
    req.encoding = req.apparent_encoding
    return req.text


if __name__ == '__main__':
    req = get_content('http://www.baidu.com')
    print(time.time()-t)
