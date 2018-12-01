#-*- coding:utf-8 _*-
#
#  File Name:    school_spider
#  Author :      lishang
#  date：        2018/11/22
#
import requests,time
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError,ReadTimeout
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {
            "Host": "www.csh.edu.cn",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "referer": "http://www.csh.edu.cn/moetc/mdepartmentExtAction!toMdepartmentExtListWdOuter.action",
            "upgrade - insecure - requests": "1",
            "cookie":"test=vlan1821_web10; COLLPIC=r8yg; test=vlan1821_web10; JSESSIONID=OMpDkI0PwX0JhxDc9mm2zqH8Hx8_BnJvRjTUE9WhC2uuZFyknpII!1989823960"
        }

basic_url = "http://www.csh.edu.cn"

# 获取代理IP
def get_proxy():
    proxy_pool_url = "http://47.93.231.162:5010/get/"
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        else:
            get_proxy()
    except ConnectionError:
        return None

def get_province():
    try:
        start_url = "http://www.csh.edu.cn/moetc/mdepartmentExtAction!toMdepartmentExtListWdOuter.action"
        html = requests.get(start_url,headers=headers,proxies={"http": "http://{}".format(get_proxy())},timeout=5)
        print(html.status_code)
        if html.status_code == 200:
            doc = pq(html.text)
            items = doc('#serId > div > div:nth-child(3) > div.h_select_line_right > a').items()
            for item in items:
                province_info = {
                    'province_name': item.text(),
                    'province_url' : basic_url + item.attr('href'),
                    'city':{}
                }
                print(province_info)
                time.sleep(1)
                for i in range(30):
                    f = get_city(province_info['province_url'])
                    if f:
                        break

                # print(f)
                province_info['city'] = f
                # print(province_info)
                save_to_mongo(province_info)

        elif html.status_code == 400:
            print("===========province超时等待===========")
            get_province()
    except (ConnectionError,ReadTimeout) as c:
            print('===========province连接超时，重新连接===========')
            get_province()

def get_city(url):
    try:
        html = requests.get(url, headers=headers, proxies={"http": "http://{}".format(get_proxy())},timeout=10)
        if html.status_code == 200:
            doc = pq(html.text)
            items = doc('#serId > div > div:nth-child(4) > div.h_select_line_right > a').items()
            city_info = {}
            for item in items:
                city = item.text()
                info = {
                    city: {
                    'city_name': item.text(),
                    'city_url' : basic_url + item.attr('href'),
                    'county':{}
                    }
                }
                # print(info)

                city_info.update(info)
                time.sleep(1)
            # print(city_info)
            return city_info

                # get_country(city_info["city_url"])
        elif html.status_code == 400:
            print("===========city超时等待===========")
            return get_city(url)
    except (ConnectionError, ReadTimeout) as c:
        print('===========city连接超时，重新连接===========')
        return get_city(url)

# def get_country(url):
#     try:
#         html = requests.get(url, headers=headers, proxies={"http": "http://{}".format(get_proxy())},timeout=10)
#         if html.status_code == 200:
#             doc = pq(html.text)
#             items = doc('#serId > div > div:nth-child(5) > div.h_select_line_right > a').items()
#             for item in items:
#                 country_info = {
#                     "country_name": item.text(),
#                     "country_url" : basic_url + item.attr('href')
#                 }
#                 print(country_info)
#
#             return country_info
#         elif html.status_code == 400:
#             print("===========超时等待===========")
#             return get_country(url)
#
#     except (ConnectionError, ReadTimeout) as c:
#         print('===========连接超时，重新连接===========')
#         return get_country(url)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('储存到mongodb成功!',result)
    except Exception:
        print('储存到mongodb失败!',result)

get_province()

