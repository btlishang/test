#-*- coding:utf-8 _*-
#
#  File Name:    mysql
#  Author :      lishang
#  date：        2018/11/25
#
import pymysql
from pymysql.err import IntegrityError

db = pymysql.connect(
    host='',
    user='',
    password='',
    db='',
    charset='utf8',
    port=3306)

def insert_content(province_id,province_name,province_url):
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO province(`province_id`,`province_name`,`province_url`) values(%s,%s,%s);"
            cursor.execute(sql, (province_id,province_name,province_url))
        db.commit()
    except IntegrityError:
        pass

def insert_city(province_id,city_id,city_name,city_url,province_name):
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO city(`province_id`,`city_id`,`city_name`,`city_url`,`province_name`) values(%s,%s,%s,%s,%s);"
            cursor.execute(sql, (province_id,city_id,city_name,city_url,province_name))
        db.commit()
    except IntegrityError:
        pass

def insert_country(province_id,city_id,country_id,country_name,country_url,city_name,province_name):
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO country(`province_id`,`city_id`,`country_id`,`country_name`,`country_url`,`city_name`,`province_name`) values(%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(sql, (province_id,city_id,country_id,country_name,country_url,city_name,province_name))
        db.commit()
    except IntegrityError:
        pass

def insert_school(province_id,city_id,country_id,province_name,city_name,country_name,school_id,school_type,school_name):
    with db.cursor() as cursor:
        sql = "INSERT INTO school(`province_id`,`city_id`,`country_id`,`province_name`,`city_name`,`country_name`,`school_id`,`school_type`,`school_name`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(sql, (province_id, city_id, country_id,province_name,city_name,country_name, school_id,school_type, school_name))
    db.commit()

# def select_country(province_id):
#     with db.cursor() as cursor:
#         sql = "SELECT * FROM country WHERE province_id = %s"
#         cursor.execute(sql,(province_id))
#         results = cursor.fetchall()
#         info = []
#         for row in results:
#             country_id = row[1]
#             country_name = row[2]
#             country_url = row[3]
#             city_id = row[4]
#             province_id = row[5]
#             city_name = row[6]
#             province_name = row[7]
#             data = [province_id,city_id,country_id,province_name,city_name,country_name,country_url]
#
#             info.append(data)
#
#             # print(province_id,city_id,country_id,country_name,country_url)
#
#     return info
def select_country(id,province_id):
    with db.cursor() as cursor:
        sql = "SELECT * FROM country WHERE id > %s and province_id = %s"
        cursor.execute(sql,(id,province_id))
        results = cursor.fetchall()
        info = []
        for row in results:
            country_id = row[1]
            country_name = row[2]
            country_url = row[3]
            city_id = row[4]
            province_id = row[5]
            city_name = row[6]
            province_name = row[7]
            data = [province_id,city_id,country_id,province_name,city_name,country_name,country_url]

            info.append(data)

            # print(province_id,city_id,country_id,country_name,country_url)

    return info

def select_city(city_name):
    with db.cursor() as cursor:
        sql = "SELECT * FROM city WHERE city_name = %s"
        cursor.execute(sql,(city_name))
        results = cursor.fetchone()


    return list(results)

def select_province(province_name):
    with db.cursor() as cursor:
        sql = "SELECT * FROM province WHERE province_name = %s"
        cursor.execute(sql,(province_name))
        results = cursor.fetchone()

    return list(results)