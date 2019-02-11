# handle url and content get request

import requests
from random import randint
from fake_useragent import UserAgent
import asyncio
from aiohttp.client import ClientSession
import time
import sys
t = time.time()
fake = UserAgent()

with open('useragent.txt', 'r', encoding='utf-8') as f:
    useragent = [i[:-1] for i in f.readlines()]
    print(time.time()-t)


# 使用代理的话中间会花很多不必要的时间， 但是如果是异步的话，可以一试
def get_proxies():
    http = requests.get('http://127.0.0.1:8080/get/http').text
    https = requests.get('http://127.0.0.1:8080/get/https').text
    # print({'http': 'http://'+http, 'https': 'https://'+https})
    return {'http': 'http://'+http, 'https': 'https://'+https}


# 堵塞式获取网页内容的接口
def get_content(url):
    useragent = fake.random
    headers = {'User-Agent': useragent}
    print(time.time()-t)
    # proxies = get_proxies()
    req = requests.get(url, headers=headers)
    # req = requests.get(url, headers=headers, proxies=proxies)
    req.encoding = 'utf-8'
    return req.text


async def asy_do(_id, url):
    async with ClientSession() as req:
        user_agent = fake.random
        headers = {'User-Agent': user_agent}
        async with req.get(url=url, headers=headers) as response:
            print('req', time.time() - t)
            text = await response.text()
    return _id, text


# 提供异步获取网页内容的接口，最好500个以上
def a_get_content(urls):
    loop = asyncio.get_event_loop()
    asyncio.Semaphore(300)
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(asy_do(*url))
        tasks.append(task)
    contents = loop.run_until_complete(asyncio.gather(*tasks))
    return contents


if __name__ == '__main__':
    req = get_content('http://www.baidu.com')
    req1 = get_content('http://www.sohu.com')
    print(time.time()-t)
    req2 = a_get_content([(1, 'http://www.baidu.com'), (2, 'http://www.sohu.com')])
    print(time.time() - t)
