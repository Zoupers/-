from bs4 import BeautifulSoup
import re
import requests
import pymysql
from urllib import request
import time


def Get_data(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
    HTMLdata = requests.get(url, headers=header).text
    return HTMLdata

#获取电影海报
def Get_movie_jpg(HTMLdata):
    soup = BeautifulSoup(HTMLdata,'html.parser')
    html = soup.find(id='content')
    datas = html.find_all(class_='pic')
    pics = []
    for data in datas:
        adr = data.a.img['src']
        obj = re.compile(r'public/(p.*?)\.jpg',re.S)
        _id = re.findall(obj,adr)
        request.urlretrieve(adr, r'C:\Users\10184\Desktop\云顶文件\movie_jpg\%s.jpg'%_id[0])
        pics.append((_id[0],r'C:\Users\10184\Desktop\云顶文件\movie_jpg\%s.jpg'%_id[0]))
    return pics

#获取电影演员照片
def Get_actor_jpg(url):
    HTMLdata = Get_data(url)
    soup = BeautifulSoup(HTMLdata, 'html.parser')
    adrs = []
    html = soup.find(class_='article')
    datas = html.find_all(class_='celebrity')
    for data in datas:
        obj = re.compile(r'https://img.*?\.jpg', re.S)
        adrs.extend(re.findall(obj,str(data)))

    result = []
    for adr in adrs:
        _id = re.findall(r'public/(.*?)\.jpg',adr)
        try:
            request.urlretrieve(adr, r'C:\Users\10184\Desktop\云顶文件\actor_jpg\%s.jpg' % _id[0])
            result.append((_id[0], r'C:\Users\10184\Desktop\云顶文件\actor_jpg\%s.jpg'%_id[0]))
        except:
            pass
    return result

#获取电影剧照
def Get_picture(url):
    HTMLdata = Get_data(url)
    soup = BeautifulSoup(HTMLdata, 'html.parser')
    adrs = []
    html = soup.find(class_='article')
    data = re.findall(r'https:.*?\.jpg',str(html))
    for adr in data:
        _id = re.findall(r'public/(.*?)\.jpg',adr)
        request.urlretrieve(adr, r'C:\Users\10184\Desktop\云顶文件\picture\%s.jpg'%_id[0])
        adrs.append((_id[0],r'C:\Users\10184\Desktop\云顶文件\picture\%s.jpg'%_id[0]))
    return adrs


#将电影所有照片整理为三个列表
def Get_all_pic(url):
    html = Get_data(url)
    movie_pic = Get_movie_jpg(html)
    soup = BeautifulSoup(html,'html.parser')
    datas = soup.find_all(class_='info')
    all_actor = []
    all_pic = []
    for data in datas:
        adr = data.div.a['href']
        _id = re.sub('\D','',adr)
        actor_adr = 'https://movie.douban.com/subject/'+str(_id)+'/celebrities'
        pic_adr = 'https://movie.douban.com/subject/'+str(_id)+'/all_photos'
        actor = Get_actor_jpg(actor_adr)
        picture = Get_picture(pic_adr)
        all_actor.extend(actor)
        all_pic.extend(picture)
    return movie_pic,all_actor,all_pic



#获取TOP250的电影海报，演员照片，剧照
movie_list =[]
actor_list =[]
picture_list =[]
for n in range(10):
    url = 'https://movie.douban.com/top250?start='+str(n*25)+'&filter='
    movie,actor,picture = Get_all_pic(url)
    movie_list.extend(movie)
    actor_list.extend(actor)
    picture_list.extend(picture)
    





#连接MySQL数据库
db = pymysql.connect(host='localhost',user='root',password='8023cltcltclt',port=3306)
cursor = db.cursor()
cursor.execute('create database picture_db character set utf8;')
cursor.execute('use picture_db')

#创建电影海报数据表
cursor.execute('create table movie(id char(20),adr char(100)) character set utf8;')
sql_insert1 = 'INSERT INTO movie(id,adr) value(%s,%s)'
try:
    cursor.executemany(sql_insert1,movie_list)
    db.commit()
except:
    print('海报数据插入失败')
    db.rollback()

#创建演员图片数据表
cursor.execute('create table actor(id char(20),adr char(100)) character set utf8;')
sql_insert2 = 'INSERT INTO actor(id,adr) value(%s,%s)'
try:
    cursor.executemany(sql_insert2,actor_list)
    db.commit()
except:
    print('演员数据插入失败')
    db.rollback()


#创建剧照数据表
cursor.execute('create table picture(id char(50),adr char(150)) character set utf8;')
sql_insert3 = 'INSERT INTO picture(id,adr) value(%s,%s)'
try:
    cursor.executemany(sql_insert3,picture_list)
    db.commit()
except:
    print('剧照数据插入失败')
    db.rollback()
