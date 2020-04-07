import os
import sqlite3
import datetime
import csv
import time

path = 'C:/Users/HP/AppData/Local/CentBrowser/User Data/Default'
files = os.listdir(path)
# 浏览器打开的时候，history文件无法访问，需要复制新的文件
history_db = os.path.join(path,'history')

c = sqlite3.connect(history_db)         # 连接数据库
cursor = c.cursor()                     # 获取游标
select_statement = "select * from urls where visit_count>=1;"
cursor.execute(select_statement)        # 创建数据库以及数据表
results = cursor.fetchall()
f = open("浏览器历史网址信息.csv",mode="w",newline="",encoding="utf-8-sig")
csv_write = csv.writer(f)
csv_write.writerow(['编号','url网址','网址名称','浏览次数','数据保存时间'])
for i in range(len(results)):
    csv_write.writerow([list(results[i])[0],list(results[i])[1],list(results[i])[2],list(results[i])[3],datetime.datetime.now()])
print(str(datetime.datetime.now()) + "\t" + "浏览器历史记录数据保存完毕！")
print("程序即将关闭！")
time.sleep(2)