
from scrapy.proxies_mine.Manager.ProxyManager import ProxyManager


def get_http():
    proxy = ProxyManager('http').get_http()
    return proxy if proxy else 'no proxy!'


def getAll_http():
    proxies = ProxyManager('http').getAll()
    return proxies


def get_https():
    proxy = ProxyManager('https').get_https()
    return proxy if proxy else 'no proxy'


def getAll_https():
    proxies = ProxyManager('https').getAll()
    return proxies


def proxies():
    http = 'http://' + get_http()
    https = 'https://' + get_https()
    return {'http': http, 'https': https}
