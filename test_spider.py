#-*- coding:utf-8 _*-
#
#  File Name:    test_spider
#  Author :      lishang
#  date：        2018/11/25

import requests,time,mysql,re
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError,ReadTimeout


headers = {
            "Host": "www.csh.edu.cn",
            # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "user-agent": "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "referer": "http://www.csh.edu.cn/moetc/mdepartmentExtAction!toMdepartmentExtListWdOuter.action",
            "upgrade - insecure - requests": "1",
            "cookie":"test=vlan1821_web10; COLLPIC=r8yg; test=vlan1821_web10; JSESSIONID=OMpDkI0PwX0JhxDc9mm2zqH8Hx8_BnJvRjTUE9WhC2uuZFyknpII!1989823960"
        }

basic_url = "http://www.csh.edu.cn"
start_url = "http://www.csh.edu.cn/moetc/mdepartmentExtAction!toMdepartmentExtListWdOuter.action"

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

def get_province(start_url):
    try:
        html = requests.get(start_url,headers=headers,proxies={"http": "http://{}".format(get_proxy())},timeout=10)
        print(html.status_code)
        if html.status_code == 200:
            doc = pq(html.text)
            items = doc('#serId > div > div:nth-child(3) > div.h_select_line_right > a').items()
            if items:
                for item in items:
                    province_name = item.text()
                    province_url = basic_url + item.attr('href')
                    province_id = item.attr('href')[70:72]
                    mysql.insert_content(province_id,province_name,province_url)

                    print("******当前省份为：-",province_name,"-******")
                    time.sleep(1)
                    get_city(province_url,province_name)
            else:
                get_province(start_url)

        elif html.status_code == 400:
            print("===========抓取省份超时",html.status_code,"，请等待===========")
            get_province(start_url)
        elif html.status_code == 503:
            print("===========抓取省份超时",html.status_code,"，请等待===========")
            get_province(start_url)

    except (ConnectionError,ReadTimeout) as c:
            print('===========省份抓取超时，重新连接中===========')
            get_province(start_url)

def get_city(url,province_name):
    try:
        html = requests.get(url, timeout=10)
        print(html.status_code)
        if html.status_code == 200:
            doc = pq(html.text)
            items = doc('#serId > div > div:nth-child(4) > div.h_select_line_right > a').items()
            for item in items:
                city_name = item.text()
                city_url = basic_url + item.attr('href')
                city_id = item.attr('href')[72:74]
                province_id = item.attr('href')[70: 72]

                mysql.insert_city(province_id,city_id,city_name,city_url,province_name)

                print("******当前城市为：-",city_name,"-******")
                time.sleep(1)
                get_country(city_url,city_name,province_name)

        elif html.status_code == 400:
            print("===========城市抓取超时，请等待===========")
            return get_city(url,province_name)

    except (ConnectionError, ReadTimeout) as c:
        print('===========抓取城市连接超时，重新连接中===========')
        return get_city(url,province_name)

def get_country(url,city_name,province_name):
    try:
        html = requests.get(url,timeout=5)
        print(html.status_code)
        if html.status_code == 200:
            doc = pq(html.text)
            items = doc('#serId > div > div:nth-child(5) > div.h_select_line_right > a').items()
            for item in items:
                country_name = item.text()
                country_url = basic_url + item.attr('href')
                country_id = item.attr('href')[-8:-6]
                province_id = item.attr('href')[-12:-10]
                city_id = item.attr('href')[-10:-8]
                mysql.insert_country(province_id,city_id,country_id,country_name,country_url,city_name,province_name)


                print("******当前县/区：-",country_name,"-******")
                time.sleep(1)

        elif html.status_code == 400:
            print("==============县/区抓取超时，请等待==============")
            return get_country(url,city_name,province_name)

    except (ConnectionError, ReadTimeout) as c:
        print('===========抓取县/区连接超时，重新连接中===========')
        return get_country(url,city_name,province_name)



if __name__ == '__main__':
    # 从头开始
    # get_province(start_url)

    # # 补充单个省
    info = mysql.select_province("山东省")
    city_url = info[3]
    province_name = info[2]
    print(city_url,province_name)
    get_city(city_url,province_name)
    # get_city()

    # # 补充单个市
    # info = mysql.select_city("抚州市")
    # city_url = info[3]
    # city_name = info[2]
    # province_name = info[5]
    # print(city_url, city_name, province_name)
    # get_country(city_url,city_name,province_name)

    mysql.db.close()