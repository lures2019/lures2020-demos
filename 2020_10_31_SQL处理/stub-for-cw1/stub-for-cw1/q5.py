"""
Q5 is a script that returns the average (across all students) raw mark for the exam. 
   
You should create and write your results into a .csv file q5Out.csv
with 1 column and the header row AverageMark

You may not import *any other modules*. This is the final and only import structure!
You will want to use the Decimal class to avoid potential rounding issues.
"""
import csv

# 计算所有学生的考试平均分
# 用到第一问的total总分
# 统计id数
# 以列表的形式将数据存储起来
f = open('exam_for_2020.csv',mode='r')
csv_reader = csv.reader(f)
rows = [i for i in csv_reader]

# Possible Points是总分,Auto Score自动评分,Manual Score手动评分
# 最后总分应该是每个id的6个问题的最后两列成绩之和（若有一列无数据则默认是0），两列仅存在一列即可
user_id = {}
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
# print(len(list(user_id.keys())))
# print(sum(list(user_id.values())))
# 创建新的csv文件
fp = open('q5Out.csv',mode='w',newline='',encoding='utf-8-sig')
csv_write = csv.writer(fp)
csv_write.writerow(['row AverageMark'])
for key,value in user_id.items():
    csv_write.writerow([sum(list(user_id.values()))/len(list(user_id.keys()))])
    break
fp.close()