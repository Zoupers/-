from scrapy.requests.g_handle import GUrlHandle
import re
from scrapy.handle_db.DBApi import DbHandle


def create_table():
    sql = '''CREATE TABLE `person`(
        `id` CHAR(15) PRIMARY KEY NOT NULL ,
        `name` CHAR(50) NOT NULL ,
        `sex` VARCHAR(5),
        `constellation` VARCHAR(10),
        `birthday` VARCHAR(30),
        `birthplace` VARCHAR(50) ,
        `profession` VARCHAR(60),
        `imdb` VARCHAR(15),
        `introduce` TEXT,
        )'''
    db = DbHandle()
    db.create_table(sql)


def get_urls():
    db = DbHandle(database='ranking')
    db.table = 'movie'
    actor_ids = db.get(_range='details')
    urls = []
    for ids in actor_ids:
        if ids[0]:
            id_list = re.findall('celebrity/(\\d*?)/', str(ids[0]))
            url_list = ['https://movie.douban.com/celebrity/%s/' % _id for _id in id_list]
            urls.extend(url_list)
        else:
            continue
    urls.remove('https://movie.douban.com/celebrity/1376098/')
    # db.table = 'person'
    # actor_ids = db.get(_range='id')
    # have_urls = []
    # for ids in actor_ids:
    #     url = 'https://movie.douban.com/celebrity/%s/' % ids
    #     have_urls.append(url)
    #
    # print(len(have_urls))
    # u = list(set(urls) ^ set(have_urls))
    # print(len(set(have_urls)), len(set(urls)))
    # print(len(u))
    # # u.remove('https://movie.douban.com/celebrity/1369442/')
    request = GUrlHandle(content_handle=content_handle, max_=400)
    request.get_contents(urls)


def content_handle(info):
    # all_actor_information = []
    _id = re.findall('id="headline".*?rel="nofollow".*?https://movie.douban.com/celebrity/(\d*?)/', info, re.S)
    data = [_id[0]]
    name = re.findall(r'<div id="content">.*?<h1>(.+)</h1>', info, re.S)[0]
    try:
        sex = re.findall(r'<span>性别<.+>:\s*(.*)\s*', info)[0]
    except:
        print('Can not find actor sex')
        sex = None
    try:
        constellation = re.findall(r'<span>星座<.+>:\s*(.*)\s*', info)[0]
    except:
        print('Can not find constellation')
        constellation = None
    try:
        birthday = re.findall(r'<span>出生日期<.+>:\s*(.*)\s*', info)[0]
    except Exception as e:
        try:
            birthday = re.findall(r'<span>生卒日期<.+>:\s*(.*)\s*', info)[0]
        except:
            print('Can not find birthday')
            birthday = None
    try:
        birthplace = re.findall(r'<span>出生地<.+>:\s*(.*)\s*', info)[0]
    except:
        print('Can not find birthplace')
        birthplace = None
    try:
        profession = re.findall(r'<span>职业<.+>:\s*(.*)\s*', info)[0]
    except:
        print('Can not find profession')
        profession = None
    try:
        imdb_number = re.findall(r'<span>imdb编号<.+>:\s*.+>(.+)</a>', info)[0]
    except:
        print('Can not find IMDB编号')
        imdb_number = None
    all_introduce = re.findall(r'<span class="all hidden">\s*(.+)<', info)
    if not bool(all_introduce):
        normal_introduce = re.findall(r'<h2>\s*影人简介\s*.+\s*<.+>\s*</div>\s*<div class="bd">\s*(.+)\s*', info)
        _dict = {
            "姓名": name,
            "性别": sex,
            "星座": constellation,
            "出生日期": birthday,
            "出生地": birthplace,
            "职业": profession,
            "imdb编号": imdb_number,
            "简介": normal_introduce[0]
        }
        # all_actor_information.append(dict)
    else:
        _dict = {
            "姓名": name,
            "性别": sex,
            "星座": constellation,
            "出生日期": birthday,
            "出生地": birthplace,
            "职业": profession,
            "imdb编号": imdb_number,
            "简介": all_introduce[0]
        }
        # all_actor_information.append(dict)
    # print(_dict)
    data.extend(_dict.values())
    if data[-1] == '</div>':
        data[-1] = None
    db = DbHandle()
    db.table = 'movie_person'
    if not db.get_by_id(_id=int(_id[0])):
        print(data)
        db.save(data)
    else:
        print('Already have this')


if __name__ == '__main__':
    # get_base_connection()
    get_urls()
























