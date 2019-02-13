# this is used to test each function
import re
from fake_useragent import UserAgent
from scrapy.requests.request_handle import AsyncGet, get_content
import time
t = time.time()
fake = UserAgent


def main():
    # response = get_content('https://movie.douban.com/top250')
    # url_find = re.findall('<a href="(https://movie.douban.com/subject/.*?)"', response)
    # print(len(url_find))
    # x = AsyncGet(url_find)
    for i in range(10):
        x = get_content('https://movie.douban.com/top250')
        # print(len(x.get_content))
        print(x)
    # for i in range(5):
    #     print(len(x.get_content[i]))
    print(time.time() - t)
    # y = get_content('http://www.baidu.com')
    # print(x.get_content, y)


if __name__ == '__main__':
    main()
