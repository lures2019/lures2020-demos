"""
Q1 is a script that returns, for each student, their ID and the total number of points they have scored. 
 
You should create and write your results into a .csv file
with 2 columns, one named "Username" (*exactly* what's between the quotes)
and "RawMark" (*exactly* what's between the quotes).

The stub contains three function stubs, `read_data_file`, `calculate_grades`, and
`write_report`. You should modify the bodies of these functions so they behave
appropriately.

You can replace the whole body of these functions if you wish, but they must be call-able
with the given arguments.
"""

# You may not import *any other modules*. This is the final and only import structure!
# You will want to use the Decimal class in case some marks are fractional (e.g., 4.5 out of 5)

import csv

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
# 创建新的csv文件
fp = open('q1Out.csv',mode='w',newline='',encoding='utf-8-sig')
csv_write = csv.writer(fp)
csv_write.writerow(['Username','RawMark'])
for key,value in user_id.items():
    csv_write.writerow([key,value])
fp.close()