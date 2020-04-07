import os
import sqlite3
import re
import datetime
import csv
import time

path = 'C:/Users/HP/AppData/Local/CentBrowser/User Data/Default'
files = os.listdir(path)
# 浏览器打开的时候，history文件无法访问，需要复制新的文件
history_db = os.path.join(path,'history')

c = sqlite3.connect(history_db)         # 连接数据库
cursor = c.cursor()                     # 获取游标
select_statement = "select urls.url,urls.visit_count from urls,visits where urls.id=visits.url;"
cursor.execute(select_statement)        # 创建数据库以及数据表
results = cursor.fetchall()
sites_count = {}

for url,count in results:
    if url in sites_count:
        sites_count[url] += 1
    else:
        sites_count[url] = 1
sites_count_sorted = sorted(sites_count.items(), key=lambda k: k[1])
results = re.findall("\((.*?)\)",str(sites_count_sorted),re.S)
f = open('浏览器搜索网址信息.csv',mode="a+",newline="",encoding="utf-8-sig")
csv_write = csv.writer(f)
csv_write.writerow(['网址url','搜索次数','数据保存时间'])
for result in results:
    try:
        if('http://' or 'https://') in result:
            csv_write.writerow([result.split(r',')[0].replace(r"'",'').strip(),result.split(r',')[1],datetime.datetime.now()])
    except:
        pass
print(str(datetime.datetime.now()) + '\t' + '网址信息保存到csv文件完毕！')
print('程序即将退出！')
time.sleep(2)