from scrapy.requests.g_handle import GUrlHandle
import re
from scrapy.handle_db.DBApi import DbHandle
from bs4 import BeautifulSoup


def comment_table_create(_id, database=None):
    # db = pymysql.connect(host='localhost', user='root', password='131421', database='ranking')
    db = DbHandle(database='comment')
    # cursor = db.cursor()
    sql = '''CREATE TABLE `%s`(
        `user_name` VARCHAR(30),
        `date` VARCHAR(30),
        `comment` TEXT
        )''' % _id
    try:
        db.execute(query=sql)
    except Exception as e:
        print(e)


def main():
    get_urls()


def get_urls():
    db = DbHandle()
    db.table = 'brief_movie'
    _id_list = db.get(_range='id')
    id_list = [i[0] for i in _id_list]
    urls = ['https://movie.douban.com/subject/%s/comments?status=P' % _id for _id in id_list]
    request = GUrlHandle(content_handle=content_handle)
    request.get_contents(urls)


def content_handle(movie):
    # movie_names = re.findall(rer1, movie, re.S)
    # print(movie_names)
    _id = list(set(re.findall('https://movie.douban.com/subject/(\\d*?)/', movie)))
    if len(_id) == 1:
        _id = _id[0]
    else:
        print(_id)
        raise Exception("!!!more than one!")
    comment_table_create(_id)
    db = DbHandle(database='comment')
    db.table = _id
    block = re.findall('id="comments".*?id="paginator"', movie, re.S)
    block = block[0]
    # soup = BeautifulSoup(movie, 'lxml')
    # comments = soup.find_all(class_='comment-item')
    pattern = 'src="(.*?)".*?class="">(.*?)<.*?comment-time.*?title="(.*?)".*?short">(.*?)<'
    comments = re.findall(pattern, block, re.S)
    # x = 1
    for comment in comments[:10]:
        data = [comment[1], str(comment[2]).replace('\n', ''), '''{}'''.format(comment[3])]
        print(_id, comment[0], comment[1], str(comment[2]).replace('\n', ''), '''{}'''.format(comment[3]))
        db.save(data)
        # 存入数据库
        # name = comment[0]
        # time = str(comment[1]).replace('\n', '').replace(' ', '')
        # word = comment[2]
        # client = pymongo.MongoClient(host='localhost', port=27017)
        # db = client.text
        # collection = db.movies
        # movie = {'电影名': movie_name, '用户名': name, '评论时间': time, '评论内容': word}
        # result = collection.insert_one(movie)
        # print(x, result)
        # x += 1


if __name__ == '__main__':
    main()
