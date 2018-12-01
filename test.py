import requests,time
#
# url = "/moetc/mdepartmentExtAction!toMdepartmentExtListWdOuter.action?cityId=113450000000&amp;mdepartmentExt.type=3&amp;mdepartmentExt.parentId=110102000000"
# city_id = url[72:74]
# print(city_id)
# print(type(city_id),len(city_id))

# url = "http://www.csh.edu.cn/moetc/mdepartmentExtAction!toMdepartmentExtListWdOuter.action?cityId=110100000000&mdepartmentExt.type=5&mdepartmentExt.parentId=110101000000"
# html = requests.get(url)
# while True:
#     time.sleep(1)
#     print(html.text,html.status_code)
#
# #             country_id = row[1]
# #             country_name = row[2]
# #             country_url = row[3]
# #             city_id = row[4]
# #             province_id = row[5]
# #             city_name = row[6]
# #             province_name = row[7]
# # data = [province_id, city_id, country_id,, province_name, city_name, country_name, country_url]

num = "4111010027"
print(num[:2])