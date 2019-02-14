from urllib import request
import time
import re
from bs4 import BeautifulSoup
import pymongo


for page in range(10):
    value = page*25
    url = 'https://movie.douban.com/top250?start=%s&filter=' % str(value)
    url = request.urlopen(url)
    time.sleep(3)
    html = url.read()
    html1 = str(html, encoding='utf-8')
    # 获取每个电影的名字和链接
    rer = r'<div class="hd">.*?<a href="(.*?)" class="">'
    urls = re.findall(rer, html1, re.S)
    url1 = [i + 'comments?status=P'for i in urls]
    # 遍历进入"全部评论"
    for url2 in url1:
        url3 = request.urlopen(url2)
        html2 = url3.read()
        movie = str(html2, encoding='utf-8')
        rer1 = r'<div id="content">.*?<h1>(.*?)</h1>'
        movie_names = re.findall(rer1, movie, re.S)
        movie_name = str(movie_names[0]).replace(' 短评', '')
        soup = BeautifulSoup(movie, 'lxml')
        comments = soup.find_all(class_='comment-item')
        rer2 = r'<a class="".*?>(.*?)</a>.*?<span class="comment-time".*?>(.*?)</span>.*?<span class="short">(.*?)</span>'
        x = 1
        for item in comments[:10]:  # 对comments列表进行切片处理，只取前十热评
            comment1 = re.findall(rer2, str(item), re.S)
            for comment in comment1:
                print(movie_name, comment[0], str(comment[1]).replace('\n', '').replace(' ', ''), comment[2])
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
