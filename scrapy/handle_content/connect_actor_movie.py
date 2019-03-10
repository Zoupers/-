from scrapy.requests.g_handle import GUrlHandle
from scrapy.handle_db.DBApi import DbHandle
import re


def get_urls():
    db = DbHandle()
    _id = db.get(table='movie', _range='id')
    urls = []
    for i in _id:
        urls.append('https://movie.douban.com/subject/{}/'.format(*i))
    session = GUrlHandle(content_handle=content_handle, max_=200, use_id=True)
    session.get_contents(urls)


def content_handle(movie_id, content):
    block = re.findall('type="application/ld\\+json".*?datePublished', content, re.S)
    # print(block)
    actors = re.findall('celebrity/(\\d*?)/', block[0])
    db = DbHandle()
    db.table = 'movie_cast'
    for actor in actors:
        try:
            if not db.get(_filter='where person_id={} and movie_id={}'.format(actor, movie_id)):
                print(actor)
                db.save(data=[movie_id, actor], _range='movie_id, person_id')
            else:
                print(movie_id, actor, 'Already have this connect')
        except Exception as e:
            # 桐本拓哉，你狠
            if actor == '1376098':
                db.save(data=[movie_id, '1250852'], _range='movie_id, person_id')
                continue
            db.close()
            print(e)


            extra(actor)
            print(actor)
            db = DbHandle()
            db.table = 'movie_cast'
            db.save(data=[movie_id, actor], _range='movie_id, person_id')


def extra(actor_id):
    import requests
    url = 'https://movie.douban.com/celebrity/%s/' % actor_id
    print('Done extra!')
    # session = GUrlHandle()
    requests.get(url, hooks={'response':lambda r, *args, **kwargs: hd(r.text)})


def hd(info):
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
    get_urls()


