# import gevent
# from gevent import monkey
# monkey.patch_all(httplib=True)
import grequests
import re
import requests
import multiprocessing
import time
from fake_useragent import UserAgent
fake = UserAgent()
requests.adapters.DEFAULT_RETRIES = 10
t = time.time()
kwargs = dict()
kwargs['timeout'] = 2
d_kwargs = dict()
d_kwargs['timeout'] = 2


class GUrlHandle(object):
    def __init__(self, content_handle=None, max_=60, use_id=False):
        self.max = max_
        self.use_id = use_id
        self.kwargs = dict()
        if content_handle:
            self.content_handle = content_handle
        self.kwargs['headers'] = {'User-Agent': fake.random}
        self.kwargs['proxies'] = self.verify(self.get_proxies())

    def verify(self, proxies):
        url = 'https://www.sohu.com'
        d_kwargs['headers'] = self.kwargs['headers']
        while True:
            try:
                d_kwargs['proxies'] = proxies
                print(proxies)
                # print(kwargs['proxies'])
                req = requests.get(url, **d_kwargs)
                print(req.status_code)
                return proxies
            except Exception as e:
                proxies = self.get_proxies()
                print(e)

    @staticmethod
    def get_proxies():
        http = requests.get('http://127.0.0.1:8080/get/http').text
        https = requests.get('http://127.0.0.1:8080/get/https').text
        # qiye
        # http = requests.get('http://127.0.0.1:8765/random?types=0&protocol=0&country=国内').text.strip('"')
        # https = requests.get('http://127.0.0.1:8765/random?types=0&protocol=1&country=国内').text.strip('"')
        # print({'http': 'http://'+http, 'https': 'https://'+https})
        return {'http': 'http://'+http, 'https': 'https://'+https}

    def get_content(self, url, hooks=None):
        kwargs['headers'] = {'User-Agent': fake.random}
        kwargs['proxies'] = self.get_proxies()
        if hooks:
            kwargs['hooks'] = {'response': hooks}
        while True:
            try:
                response = requests.get(url, **kwargs)
                if response.status_code != 200:
                    raise Exception("异常")
                print(response.url, "OK", time.time() - t)
                return response.text
            except Exception as e:
                print(e)
                kwargs['proxies'] = self.verify(self.get_proxies())

    def get_contents(self, urls):
        max = self.max
        if len(urls) <= max:
            return self._get_contents(urls)
        n = 0
        urls = list(set(urls))
        l = len(urls)
        for i in range(max, l, max):
            print(n, i)
            url = urls[n:i]
            while True:
                try:
                    self._get_contents(url)
                    break
                except Exception as e:
                    print(e)
                    # self.kwargs['proxies'] = self.get_proxies()
            n = i
            if l - i <= max:
                url = urls[i:l]
                while True:
                    try:
                        self._get_contents(url)
                        break
                    except Exception as e:
                        print(e)
                        # self.kwargs['proxies'] = self.get_proxies()

    # 每n个用一个
    def _get_contents(self, urls):
        kwargs['proxies'] = self.verify(self.get_proxies())
        kwargs['hooks'] = {'response': self.hook}
        print("G event")
        req = []
        for url in urls:
            req.append(grequests.get(url, **kwargs))
        grequests.map(req, exception_handler=self.again)
        print('G END')
        print(time.time() - t)

    def hook(self, r, *args, **kwargs):
        # print('r.status_code from hook', r.status_code)
        if self.use_id:
            _id = re.findall('https://movie.douban.com/subject/(.*?)/', r.url)[0]
            if r.status_code == 200:
                # print(r.text)
                self.content_handle(_id, r.text)
            else:
                raise Exception("NOT 200")
        else:
            if r.status_code == 200:
                # print(r.text)
                self.content_handle(r.text)
            else:
                raise Exception("NOT 200")
        return r

    # grequests 的 exception_handler
    def again(self, request, exception):
        print("Get Again Exception %s" % exception)
        kwargs = dict()
        kwargs['headers'] = self.kwargs['headers']
        kwargs['proxies'] = self.get_proxies()
        kwargs['timeout'] = 2
        kwargs['hooks'] = {'response': self.hook}
        n = 0
        while True:
            n += 1
            if n == 10:
                del kwargs['proxies']
            if n == 20:
                break
            # time.sleep(1)
            print("%s 第%s次重试" % (request.url, n))
            try:
                result = requests.get(request.url, **kwargs)
                if result.status_code == 200:
                    break
            except Exception as e:
                print(e)
                kwargs['proxies'] = self.get_proxies()


def test_handle(r, *args, **kwargs):
    # _id = re.findall('https://movie.douban.com/subject/(\\d*?)/', r.url)[0]
    # with open('d://test/%s.html' % _id, 'w', encoding='utf-8') as f:
    #     f.write(r)
    #     print(_id, "OK", time.time() - t)
    print(r[400:1000])


def devide(urls):
    urls = list(set(urls))
    n = 0
    l = len(urls)
    for i in range(100, l, 100):
        yield urls[n:i]
        n = i
        if l - n <= 100:
            yield urls[n:l]
            break


def test():
    final_urls = []
    x = GUrlHandle(test_handle)
    for i in range(10):
        response = x.get_content('https://movie.douban.com/top250?start=%s&filter=' % (25 * i))
        urls = re.findall('<a href="(https://movie.douban.com/subject/.*?)"', response)
        final_urls.extend(urls)
    # x.get_contents(final_urls)
    pool = multiprocessing.Pool()
    pool.starmap_async(x.get_contents, [(url,) for url in devide(final_urls)], callback=lambda *args, **kwargs: print("OK"))
    pool.close()
    pool.join()
    # print(len(contents))
    # for n, i in zip(range(1, len(contents)+1), contents):
    #     with open("d://test//%s.html" % n, 'wb') as f:
    #         f.write(i)
    #     print(dir(i), i)
    print(time.time() - t)


if __name__ == '__main__':
    test()



