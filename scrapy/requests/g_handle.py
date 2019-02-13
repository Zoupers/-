# import gevent
# from gevent import monkey
# monkey.patch_all(httplib=True)
import grequests
import re
import requests
import time
from multiprocessing import Process, Queue
from threading import Thread
t = time.time()
kwargs = dict()
q = Queue()


class GUrlHandle(object):
    def __init__(self, content_handle):
        self.kwargs = dict()
        self.content_handle = content_handle
        self.useragent = [
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET CLR 1.1.4322; .NET4.0C; Tablet PC 2.0)',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
        ]
        self.n = 0
        self.kwargs['headers'] = {'User-Agent': self.useragent[self.n]}
        self.kwargs['proxies'] = self.verify(self.get_proxies())

    def verify(self, proxies):
        url = 'https://www.sohu.com'
        while True:
            try:
                kwargs['proxies'] = proxies
                print(proxies)
                kwargs['timeout'] = 5
                # print(kwargs['proxies'])
                req = requests.get(url, **kwargs)
                print(req.status_code)
                return proxies
            except Exception as e:
                proxies = self.get_proxies()
                print(e)

    @staticmethod
    def get_proxies():
        http = requests.get('http://127.0.0.1:8080/get/http').text
        https = requests.get('http://127.0.0.1:8080/get/https').text
        # print({'http': 'http://'+http, 'https': 'https://'+https})
        return {'http': 'http://'+http, 'https': 'https://'+https}

    def get_content(self, url, hooks=None):
        kwargs['headers'] = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
        kwargs['timeout'] = 5
        if hooks:
            kwargs['hooks'] = {'response': hooks}
        while True:
            try:
                return requests.get(url, **kwargs).text
            except requests.exceptions.ProxyError as e:
                kwargs['proxies'] = self.verify(self.get_proxies())
                pass

    def get_contents(self, urls):
        if len(urls) <= 60:
            return self._get_contents(urls)
        n = 0
        l = len(urls)
        for i in range(60, l, 60):
            print(type(n), n, type(i), i)
            url = urls[n:i]
            while True:
                try:
                    self._get_contents(url)
                    break
                except Exception as e:
                    self.n += 1
                    if self.n == len(self.useragent):
                        self.n = 0
                    self.kwargs['proxies'] = self.get_proxies()
            n = i
            if l - i <= 60:
                url = urls[i:l]
                self._get_contents(url)
                break

    # 每一百个用一个
    def _get_contents(self, urls):
        kwargs['proxies'] = self.verify(self.get_proxies())
        kwargs['hooks'] = {'response': self.hook}
        print("G event")
        req = []
        for url in urls:
            req.append(grequests.get(url, **kwargs))
        contents = grequests.map(req, exception_handler=self.again)
        print('G END')
        print(time.time() - t)

    def hook(self, r, *args, **kwargs):
        if not r.text:
            self.content_handle(r.text)
        return r

    # grequests 的 exception_handler
    def again(self, request, exception):
        print("Get Again Exception %s" % exception)
        kwargs = dict()
        kwargs['headers'] = self.kwargs['headers']
        kwargs['proxies'] = self.get_proxies()
        kwargs['hooks'] = {'response': self.content_handle}
        n = 0
        # try:
            # del self.kwargs['timeout']
        # except Exception as e:
            # print(e)
        while True:
            n += 1
            print("%s 第%s次重试" % (request.url, n))
            try:
                requests.get(request.url, **kwargs)
            except Exception as e:
                print(e)
                kwargs['proxies'] = self.get_proxies()


def test():
    final_urls = []
    x = GUrlHandle(lambda a: print(getattr(a, 'text', 'None')))
    for i in range(1):
        response = x.get_content('https://movie.douban.com/top250?start=%s&filter=' % (25 * i))
        urls = re.findall('<a href="(https://movie.douban.com/subject/.*?)"', response)
        final_urls.extend(urls)
    x.get_contents(final_urls)
    # print(len(contents))
    # for n, i in zip(range(1, len(contents)+1), contents):
        # with open("d://test//%s.html" % n, 'wb') as f:
        #     f.write(i)
        # print(dir(i), i)
    print(time.time() - t)


if __name__ == '__main__':
    test()



