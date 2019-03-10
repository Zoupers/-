from scrapy.requests.g_handle import GUrlHandle
from scrapy.handle_db.DBApi import DbHandle
import requests
import os
import re
from fake_useragent import UserAgent
from lxml import etree

SOURCE = r'D:\桌面\python\python库学习\scrapy\wuyanspider\wuyanspider\source'


class Main(object):

    def __init__(self):
        self.db = DbHandle(database='spider')
        self.cursor = self.db.cursor
        self.fake = UserAgent()

    def get_urls(self):
        self.db.table = 'ranking'
        _id_list = self.db.get(_range='movie_id')
        id_list = list(set([i[0] for i in _id_list]))
        self.cursor.execute('use `spider_comment`')
        self.cursor.execute('show tables')
        tables = self.cursor.fetchall()
        for i in tables:
            try:
                id_list.remove(i[0])
            except ValueError as e:
                id_list.append(i[0])
        # 处理评论
        comments_urls = ['https://movie.douban.com/subject/%s/comments?status=P' % _id for _id in id_list]
        print(comments_urls)
        # 处理电影
        movies_urls = ['https://movie.douban.com/subject/%s/' % _id for _id in id_list]
        # 处理获奖
        for m, i in zip(id_list, comments_urls):
            requests.get(i, hooks={'response': lambda r, *args, **kwargs : self.comments_handle(m, r.text)})
        # request = GUrlHandle(content_handle=self.comments_handle, use_id=True)
        # request.get_contents(comments_urls)

    def comments_handle(self, _id, text):
        # html = etree.HTML(text)
        # t = html.xpath('//a/@href')
        self.cursor.execute('USE `spider_comment`')
        movie_id = _id
        self.cursor.execute('SHOW TABLES')
        all_table = self.cursor.fetchall()
        if (movie_id,) not in all_table:
            try:
                s = 'CREATE TABLE ' + '`' + movie_id + '`'
                self.cursor.execute('''
                        {}(
                        `user_id` VARCHAR(30),
                        `user_name` VARCHAR(30),
                        `comment_time` DATETIME,
                        `comment` TEXT,
                        `image` VARCHAR(50)
                        )
                        '''.format(s))
            except Exception as e:
                print(e)

            comments = re.findall('class="avatar".*?title="(.*?)".*?"https://www.douban.com/people/(.*?)/".*?src="(.*?)".*?<.*?comment-time.*?title="(.*?)".*?short">(.*?)<', text, re.S)
            for comment_ in comments:
                # [comment[1], comment[0], str(comment[3]).replace('\n', ''), '''{}'''.format(comment[4])]
                user_id = comment_[1]
                user_name = comment_[0]
                comm_time = str(comment_[3]).replace('\n', '')
                comm = comment_[4]
                image = re.sub('/u(.*?)-.*?\\.', '/ul\\1.', comment_[2])
                pic = user_id+'.jpg'
                pic_path = os.path.join('user', pic)
                with open(os.path.join(SOURCE, pic_path), 'wb') as f:
                    f.write(requests.get(image, {'User-Agent': self.fake.random}).content)
                image = pic_path
                sql = 'INSERT INTO ' + '`' + movie_id + '`'
                self.cursor.execute(
                    sql + '(`user_id`, `user_name`, `comment_time`, `comment`,`image`) VALUES(%s, %s, %s, %s, %s)',
                    [user_id, user_name, comm_time, comm, image])
                self.db.commit()
                print(user_id, user_name, comm_time, comm, image)


if __name__ == '__main__':
    main = Main()
    main.get_urls()


