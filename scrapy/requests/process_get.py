from multiprocessing import Process, Pool
import requests
from fake_useragent import UserAgent
import time
fake = UserAgent()
t = time.time()
requests.adapters.DEFAULT_RETRIES = 5
error_urls = []


def get_proxies(x=False, y=False):
    http = requests.get('http://127.0.0.1:8080/get/http').text
    https = requests.get('http://127.0.0.1:8080/get/https').text
    # print({'http': 'http://'+http, 'https': 'https://'+https})
    if x:
        return https.split(':')[0]
    if y:
        return http.split(':')[0]
    return {'http': 'http://'+http, 'https': 'https://'+https}


def handle(r, *args, **kwargs):
    print(r.url, args, kwargs)
    print(time.time() - t)
    return r


class Get(object):
    def __init__(self, urls=None, content_handle=None, callback=None):
        self.error_urls = []
        self.urls = urls

        if content_handle:
            self.handler = content_handle
        else:
            self.handler = handle
        if callback:
            self._back = callback
        else:
            self._back = back
        self.pool = Pool(20)
        self.kwargs = dict()
        self.kwargs['headers'] = {'User-Agent': fake.random}
        self.kwargs['proxies'] = get_proxies()
        # self.kwargs['verify'] = False
        self.kwargs['timeout'] = 5
        self.kwargs['hooks'] = {'response': self.handler}

    def get_by_pool(self, urls=None):
        if urls:
            self.urls = urls
        self.pool.starmap_async(req, [(url, self.kwargs) for url in self.urls], callback=self._back, error_callback=self.error_handle)
        self.pool.close()
        self.pool.join()

    def error_handle(self, e):
        if len(self.error_urls) != 0:
            self.get_by_pool(urls=self.error_urls)
        print(e)


def get(urls, content_handle=None, callback=None):
    if content_handle:
        handler = content_handle
    else:
        handler = handle
    if callback:
        _back = callback
    else:
        _back = back
    pool = Pool(10)
    kwargs = dict()
    kwargs['headers'] = {'User-Agent': fake.random}
    kwargs['headers']['Cache-Control'] = 'max-age=0'
    kwargs['headers']['Accept-Language'] = 'zh-CN,zh;q=0.9'
    kwargs['headers']['Accept-Encoding'] = 'gzip, deflate, br'
    kwargs['proxies'] = get_proxies()
    kwargs['timeout'] = 5
    kwargs['Keep-Alive']=False
    kwargs['hooks'] = { 'response': handler}
    pool.starmap_async(req, [(url, kwargs) for url in urls], callback=_back, error_callback=_back)
    pool.close()
    pool.join()


def req(url, kwargs):
    try:
        s = requests.Session()
        headers = {'User-Agent': fake.random}
        proxies = get_proxies()
        s.keep_alive = False
        response = s.get(url, headers=headers, proxies=proxies, timeout=5)
        return response
    except Exception as e:
        error_urls.append(url)
        print(e)
        print("Have got %d error url" % len(error_urls))
        if len(error_urls) == 20:
            print("Handle Error URLS")
            g = Get()
            g.get_by_pool(urls=error_urls)
            error_urls.clear()


def back(r, *args, **kwargs):
    print("Here is callback")
    print(r, args, kwargs)
    return


class urls_handle(object):
    def __init__(self, urls, content_handle=None, callback=None):
        self.urls = urls
        self.content_handle = content_handle
        if callback:
            self.callback = callback

    def run(self):
        if len(self.urls) <= 20:
            z = Get(urls=self.urls, content_handle=self.content_handle)
            z.get_by_pool()
            return
        n = 0
        z = Get(content_handle=self.content_handle)
        for i in range(0, len(self.urls), 20):
            z.get_by_pool(urls=self.urls[n:i])
            print(n)
            n = i


def test():
    import json
    from scrapy.handle_db.DBApi import DbHandle
    db = DbHandle()
    urls = json.loads(db.get(table='init')[0][1])
    for i in urls:
        print(i)
    h = urls_handle(urls)
    h.run()



if __name__ == '__main__':
    test()

