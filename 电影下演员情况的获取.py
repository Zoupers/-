import re
import requests
from fake_useragent import UserAgent
import time


def get_base_connection():
    base_url = "https://movie.douban.com/top250?"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    film_connection = []
    for num in range(10):
        params = {
            "start": num * 25
        }
        response = requests.get(base_url, headers=headers, params=params)
        info = response.text
        connection = re.findall(r'<div class="hd">\s+<a href="(.+)" ', info)
        film_connection.extend(connection)
    get_every_connection(film_connection)


def get_every_connection(film_connection):
    base_url = "https://movie.douban.com{}"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    every_actor_connection = []
    for url in film_connection:
        response = requests.get(url, headers=headers)
        info = response.text
        actor_connection = re.findall(r'class="c.+s">\s*<h2>\s*.+\s*.+\s*.+\s*.\s*<a href="(.+)">', info)
        new_url = base_url.format(actor_connection[0])
        every_actor_connection.append(new_url)
    handle_actors(every_actor_connection)


def handle_actors(every_actor_connection):
    headers = {
        "User-Agent": UserAgent().chrome
    }
    all_film_actors = []
    for url in every_actor_connection:
        list = []
        response = requests.get(url, headers=headers)
        info = response.text
        director_name = re.findall(r'<h2>导演 .+\s*.+\s*.+\s*.+ title="(.+)" c', info)
        director_acts = re.findall(r'<h2>导演 .+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+title="(.+)">', info)
        director_dict = handle_dict(director_name, director_acts)
        list.extend(director_dict)
        cast_name = re.findall(r'<h2>演员 .+\s*.+\s*.+\s*.+ title="(.+)" c', info)
        cast_acts = re.findall(r'<h2>演员 .+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+title="(.+)">', info)
        cast_dict = handle_dict(cast_name, cast_acts)
        list.extend(cast_dict)
        writer_name = re.findall(r'<h2>编剧 .+\s*.+\s*.+\s*.+ title="(.+)" c', info)
        writer_acts = re.findall(r'<h2>编剧 .+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+\s*.+title="(.+)">', info)
        writer_dict = handle_dict(writer_name, writer_acts)
        list.extend(writer_dict)
        all_film_actors.append(list)
        time.sleep(3)
    print(all_film_actors)


def handle_dict(actor_name, actor_acts):
    a_dict = []
    mixing = zip(actor_name, actor_acts)
    for name, acts in mixing:
        dict = {
            "姓名": name,
            "职位": acts,
        }
        a_dict.append(dict)
    return a_dict


if __name__ == '__main__':
    get_base_connection()
