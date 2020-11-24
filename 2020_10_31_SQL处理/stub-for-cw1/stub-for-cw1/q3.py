"""
Q3 is a script that returns, for each student, their ID, the number of points 
scored on the autograded questions, the number of points scored on the manually graded 
  questions, and total number of points scored. 
   
You should create and write your results into a .csv file q3Out.csv
with 4 columns and the header row Username, RawAutogradedMark, RawManualMark, RawTotalMark.

You may not import *any other modules*. This is the final and only import structure!
You will want to use the Decimal class to avoid potential rounding issues.
"""

import csv

# 总得分再第一问已经得出
# 本问需统计 自动评分和手动评分的分数和分别是多少
# 以列表的形式将数据存储起来
f = open('exam_for_2020.csv',mode='r')
csv_reader = csv.reader(f)
rows = [i for i in csv_reader]

# Possible Points是总分,Auto Score自动评分,Manual Score手动评分
# 最后总分应该是每个id的6个问题的最后两列成绩之和（若有一列无数据则默认是0），两列仅存在一列即可
user_id = {}
auto_id = {}
manual_id = {}
for row in rows[1:]:
    total = 0
    manual = 0
    auto = 0
    # 后面两列必然有一列是有数值的
    if len(row[5]) == 0:
        row[5] = 0
        manual += float(row[6])
    if len(row[6]) == 0:
        row[6] = 0
        auto += float(row[5])
    total += (float(row[5]) + float(row[6]))
    if row[0] not in user_id:
        user_id[row[0]] = total
    else:
        user_id[row[0]] += total
    if row[0] not in auto_id:
        auto_id[row[0]] = auto
    else:
        auto_id[row[0]] += auto
    if row[0] not in manual_id:
        manual_id[row[0]] = manual
    else:
        manual_id[row[0]] += manual

# 创建新的csv文件
fp = open('q3Out.csv',mode='w',newline='',encoding='utf-8-sig')
csv_write = csv.writer(fp)
csv_write.writerow(['Username', 'RawAutogradedMark', 'RawManualMark', 'RawTotalMark'])
for key,value in user_id.items():
    csv_write.writerow([key,auto_id[key],manual_id[key],value])
fp.close()