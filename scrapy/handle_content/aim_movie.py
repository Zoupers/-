from scrapy.requests.g_handle import GUrlHandle
from scrapy.handle_db.DBApi import DbHandle
import requests
import os
import re
import json
from fake_useragent import UserAgent
from lxml import etree

SOURCE = r'D:\桌面\python\python库学习\scrapy\wuyanspider\wuyanspider\source'


class Main(object):

    def __init__(self):
        self.db = DbHandle()
        self.cursor = self.db.cursor
        self.fake = UserAgent()

    def get_urls(self):
        db = DbHandle(database='spider')
        self.db.table = 'ranking'
        _id_list = db.get(table='ranking', _range='movie_id')
        id_list = list(set([i[0] for i in _id_list]))
        done_ = db.get(table='spider_movie', _range='id')
        # print(done_)
        print(len(id_list))
        for i in done_:
            id_list.remove(i[0])
        print(len(id_list))
        # 处理评论
        # comments_urls = ['https://movie.douban.com/subject/%s/comments?status=P' % _id for _id in id_list]
        # 处理电影
        movies_urls = ['https://movie.douban.com/subject/%s/' % _id for _id in id_list]
        # 处理获奖
        for m, i in zip(id_list, movies_urls):
            requests.get(i, hooks={'response': lambda r, *args, **kwargs : self.movie_handle(m, r.text)})
        # request = GUrlHandle(content_handle=self.movie_handle, use_id=True)
        # request.get_contents(movies_urls)

    def movie_handle(self, _id, t):
        movie_id = _id
        print(movie_id)
        self.cursor.execute('USE `spider`')
        response = etree.HTML(t)
        # response = html.xpath('//a/@href')
        try:
            name = response.xpath('//*[@id="content"]/h1/span[1]/text()')[0].split()[0]
        except:
            print(response.xpath('//*[@id="content"]/h1/text()'))
            return
        try:
            rank = re.findall('ratingValue": "(.*?)"', t, re.S)[0]
        except:
            rank = '0.0'
        if rank == '':
            rank = '0.0'
        try:
            star_num = re.findall('ratingCount": "(.*?)"', t, re.S)[0]
        except:
            star_num = None
        try:
            year = re.findall('datePublished": "(.*?)"', t, re.S)[0]
        except:
            year = None
        try:
            _class = json.dumps(json.loads(re.findall('genre": (\[.*?\])', t, re.S)[0]), ensure_ascii=False)
        except:
            _class = None
        try:
            countries = re.findall('制片国家/地区:</span> (.*?)<', t)[0]
        except:
            countries = None
        try:
            long = response.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')[0]
        except:
            long = None
        poster = response.xpath('//*[@id="mainpic"]/a/img/@src')[0]
        pic = movie_id + '.jpg'
        pic_path = os.path.join('movie', pic)
        with open(os.path.join(SOURCE, pic_path), 'wb') as f:
            f.write(requests.get(poster, {'User-Agent': self.fake.random}).content)
        poster = pic_path
        review = None
        content = ''
        contents = response.xpath('//span[@class="all hidden"]/text()')
        if contents:
            for i in contents:
                content += i.strip()
        else:
            for i in response.xpath('//span[@property="v:summary"]/text()'):
                content += i.strip()
        details = content
        # 对电影剧照的收集
        images = response.xpath('//*[@id="related-pic"]/ul/li')
        image = []
        for image_ in images:
            img = image_.xpath('./a/img/@src')
            image.extend(img)
        _image = []
        for n, i in enumerate(image):
            pic = movie_id + '_' + str(n) + '.jpg'
            pic_path = os.path.join('movie', pic)
            with open(os.path.join(SOURCE, pic_path), 'wb') as f:
                f.write(requests.get(i, {'User-Agent': self.fake.random}).content)
            _image.append(pic_path.replace('\\', '/'))
        image = json.dumps(_image)
        if not self.cursor.execute('SELECT `movie_name` FROM `spider_movie` WHERE id=%s', _id):
            self.cursor.execute('''
            INSERT INTO `spider_movie`(
            `movie_name`,
            `long`,
            `rank`,
            `star_num`,
            `year`,
            `class`,
            `countries`,
            `id`,
            `review`,
            `details`,
            `poster`,
            `image`
            ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', [
                name,
                long,
                rank,
                star_num,
                year,
                _class,
                countries,
                _id,
                review,
                details,
                poster,
                image
            ])
            self.db.commit()
            print([
                    name,
                    long,
                    rank,
                    star_num,
                    year,
                    _class,
                    countries,
                    _id,
                    review,
                    details,
                    poster,
                    image
                ])


if __name__ == '__main__':
    main = Main()
    main.get_urls()
