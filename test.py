# this is used to test each function

from scrapy.requests.request_handle import AsyncGet, get_content


def main():
    x = AsyncGet(['http://www.baidu.com', 'http://www.sohu.com'])
    y = get_content('http://www.baidu.com')
    print(x.a_get_content, y)


if __name__ == '__main__':
    main()
