#-*- coding:utf-8 _*-
#
#  File Name:    spider
#  Author :      lishang
#  date：        2018/11/24
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
# from requests.exceptions.RequestException import
from pyquery import PyQuery as pq
import requests,time,re
import mysql

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

# options = webdriver.ChromeOptions()
# options.add_argument('--proxy-server=' + "http://{}".format(get_proxy()))
# options.add_argument("headless")
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)



def get_info(province_id,city_id,country_id,province_name,city_name,country_name,country_url):
    try:
        browser.get(country_url)
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#btmSpan > span.totalPages')))
        get_products(country_id,city_id,province_id,province_name,city_name,country_name)
        return total.text
    except TimeoutException:
        return get_info(province_id,city_id,country_id,province_name,city_name,country_name,country_url)

def get_products(country_id,city_id,province_id,province_name,city_name,country_name):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#senfe > tbody')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#senfe > tbody > tr').items()
    for item in items:
        school_name = item.find('td.h_tdListCenter').text()
        school_id = item.find('td.h_tdListCenter1').text()
        if school_id[:2] == "36":
            school_type = "中等职业学校教育"
        elif school_id[:2] == "34":
            school_type = "普通高中教育"
        elif school_id[:2] == "31":
            school_type = "普通初中教育"
        elif school_id[:2] == "21":
            school_type = "普通小学教育"
        elif school_id[:2] == "10":
            school_type = "学前教育"
        elif school_id[:2] == "22":
            school_type = "成人小学教育"
        elif school_id[:2] == "32":
            school_type = "职业初中教育"
        elif school_id[:2] == "33":
            school_type = "成人初中教育"
        elif school_id[:2] == "35":
            school_type = "成人高中教育"
        elif school_id[:2] == "41":
            school_type = "普通高等教育"
        elif school_id[:2] == "42":
            school_type = "成人高等教育"
        elif school_id[:2] == "50":
            school_type = "特殊教育"
        elif school_id[:2] == "91":
            school_type = "职业技能培训"
        elif school_id[:2] == "92":
            school_type = "体校及体育培训"
        elif school_id[:2] == "93":
            school_type = "文化艺术培训"
        elif school_id[:2] == "94":
            school_type = "教育辅助服务"
        elif school_id[:2] == "99":
            school_type = "其他未列明教育"
        else:
            school_type = "其他"
        country_id = country_id
        city_id = city_id
        province_id = province_id
        mysql.insert_school(province_id,city_id,country_id,province_name,city_name,country_name,school_id,school_type,school_name)
        print(school_name,school_id)
    # time.sleep(1)

# 通过选项卡跳转

def next_page(classSelectText,province_id,city_id,country_id,province_name,city_name,country_name):
    try:
        Select(browser.find_element_by_css_selector("#toAppointedPage")).select_by_visible_text(classSelectText)
        get_products(country_id,city_id,province_id,province_name,city_name,country_name)
        time.sleep(1)
    except TimeoutException:
        next_page(classSelectText,province_id,city_id,country_id,province_name,city_name,country_name)

# 通过输入框跳转

# def next_page(page_number,province_id,city_id,country_id,province_name,city_name,country_name):
#     try:
#         input = wait.until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '#toAppointedPageInput'))
#         )
#         submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#toAppointedPageSubmit')))
#         input.clear()
#         input.send_keys(page_number)
#         submit.click()
#         # wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#disabledPage'),str(page_number)))
#         get_products(country_id, city_id, province_id, province_name, city_name, country_name)
#     except TimeoutException:
#         next_page(page_number,province_id,city_id,country_id,province_name,city_name,country_name)

def main():
    infos = mysql.select_country(3419,46)
    for info in infos:
        province_id = info[0]
        city_id = info[1]
        country_id = info[2]
        province_name = info[3]
        city_name = info[4]
        country_name = info[5]
        country_url = info[6]

        print("当前抓取地名：",country_name,"当前节点:",country_id,"省节点：",province_id,"市节点：",city_id)

        # 抓取第一级、省市大学
        # mes = mysql.select_province(province_name)
        # province_id = mes[0]
        # city_id = 1
        # country_id = mes[0]
        # province_name = mes[1]
        # city_name = mes[1]
        # country_name = mes[1]
        # country_url = mes[2]

        total = get_info(province_id,city_id,country_id,province_name,city_name,country_name,country_url)
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2,total + 1):
            next_page(str(i),province_id,city_id,country_id,province_name,city_name,country_name)
            time.sleep(1)
        # browser.close()
        time.sleep(1)
if __name__ == '__main__':
    main()
    mysql.db.close()
    browser.close()
