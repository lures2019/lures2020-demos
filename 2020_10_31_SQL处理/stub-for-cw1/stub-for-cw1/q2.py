"""
Q2 is a script that returns, for each student, their ID and
the percentage (of all available points) they have scored. 
   
You should create and write your results into a .csv file q2Out.csv
 with 2 columns and the header row Username and PercentageMark.

You may not import *any other modules*. This is the final and only import structure!
You will want to use the Decimal class to avoid potential rounding issues.
"""

import csv

# 第一问统计的便是每个id获得的6个问题的总分
# 本问是获取6个id的posiable points的总分，一除便是
# 以列表的形式将数据存储起来
f = open('exam_for_2020.csv',mode='r')
csv_reader = csv.reader(f)
rows = [i for i in csv_reader]

# Possible Points是总分,Auto Score自动评分,Manual Score手动评分
# 最后总分应该是每个id的6个问题的最后两列成绩之和（若有一列无数据则默认是0），两列仅存在一列即可
user_id = {}
posiable_points = {}
for row in rows[1:]:
    total = 0
    if len(row[5]) == 0:
        row[5] = 0
    if len(row[6]) == 0:
        row[6] = 0
    total += (float(row[5]) + float(row[6]))
    if row[0] not in user_id:
        user_id[row[0]] = total
    else:
        user_id[row[0]] += total
    if row[0] not in posiable_points:
        posiable_points[row[0]] = float(row[4])
    else:
        posiable_points[row[0]] += float(row[4])
# 创建新的csv文件
fp = open('q2Out.csv',mode='w',newline='',encoding='utf-8-sig')
csv_write = csv.writer(fp)
csv_write.writerow(['Username','PercentageMark'])
for key,value in user_id.items():
    csv_write.writerow([key,'{:.2f}%'.format(value/posiable_points[key]*100)])
fp.close()