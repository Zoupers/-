# handle url and content get request

import requests
from fake_useragent import UserAgent
import asyncio
from aiohttp.client import ClientSession
# import time
fake = UserAgent()
# t = time.time()


# 使用代理的话中间会花很多不必要的时间， 但是如果是异步的话，可以一试
def get_proxies(x=False, y=False):
    http = requests.get('http://127.0.0.1:8080/get/http').text
    https = requests.get('http://127.0.0.1:8080/get/https').text
    # print({'http': 'http://'+http, 'https': 'https://'+https})
    if x:
        return https.split(':')[0]
    if y:
        return http.split(':')[0]
    return {'http': 'http://'+http, 'https': 'https://'+https}


proxies = get_proxies()


# 堵塞式获取网页内容的接口
def get_content(url, hook=None):
    useragent = fake.random
    # print(time.time()-t)
    # proxies = get_proxies()
    kwargs = dict()
    kwargs['headers'] = {'User-Agent': useragent}
    if hook:
        kwargs['hooks'] = {'response': hook}
    # 避免出现没用的代理
    while True:
        proxies = get_proxies()
        try:
            kwargs['proxies'] = proxies
            # print(kwargs['proxies'])
            req = requests.get(url, **kwargs)
            break
        except Exception as e:
            print(e)
    req.encoding = 'utf-8'
    return req.text


class AsyncGet(object):
    """
    异步获取urls:list的内容
    """
    def __init__(self, urls: "a list of urls",
                 # proxy=False
                 x_forwarded_for=None
                 ):
        """
        :type urls: list of urls
        """
        self.urls = urls
        if x_forwarded_for:
            self.x_forwarded_for = x_forwarded_for
        else:
            self.x_forward_for = None

    async def asy_do(self, url):
        async with ClientSession() as req:
            user_agent = fake.random
            kwargs = dict()
            kwargs['headers'] = {'User-Agent': user_agent}
            if self.x_forwarded_for:
                kwargs['headers']['X-Forwarded-For'] = get_proxies(x=True)
                print(kwargs['headers']['X-Forwarded-For'])
                kwargs['headers']['X-Client-IP'] = get_proxies(y=True)
                kwargs['headers']['X-Remote-IP'] = get_proxies(y=True)
                kwargs['headers']['X-Remote-Addr'] = get_proxies(x=True)
                kwargs['headers']['X-Originating-IP'] = get_proxies(y=True)
            async with req.get(url=url, **kwargs) as response:
                # print('req', time.time() - t)
                text = await response.text()
        return text

    # 提供异步获取网页内容的接口，最好500个以上
    @property
    def get_content(self):
        loop = asyncio.get_event_loop()
        asyncio.Semaphore(300)
        tasks = []
        for url in self.urls:
            task = asyncio.ensure_future(self.asy_do(url))
            tasks.append(task)
        contents = loop.run_until_complete(asyncio.gather(*tasks))
        # print(time.time() - t)
        # 返回的是网页内容的集合
        return contents


if __name__ == '__main__':
    req = get_content('http://www.baidu.com')
    req1 = get_content('http://www.sohu.com')
    # print(time.time()-t)
    req2 = AsyncGet(urls=['http://www.baidu.com', 'http://www.sohu.com'],
                    # proxy=True
                    )
    print(req2.get_content)
    # print(time.time() - t)
