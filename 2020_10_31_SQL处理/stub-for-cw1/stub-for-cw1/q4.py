"""
Q4 is a script that returns, for each question, the question ID and the number of
students  who have passed this question (assuming that a student passes a 
question if they score at least half the points possible). 
   
You should create and write your results into a .csv file q4Out.csv
with 2 columns and the header row Question ID, StudentsPassed. 

You may not import *any other modules*. This is the final and only import structure!
You will want to use the Decimal class to avoid potential rounding issues.
"""

import csv

# 对于每一个question id，计算通过本题的学生数
f = open('exam_for_2020.csv')
csv_reader = csv.reader(f)
rows = [i for i in csv_reader]

question_id_passed = {}
for row in rows[1:]:
    total = 0
    if len(row[5]) == 0:
        row[5] = 0
    if len(row[6]) == 0:
        row[6] = 0
    total += (float(row[5]) + float(row[6]))
    if total > float(row[4])/2:
        if row[3] not in question_id_passed:
            question_id_passed[row[3]] = 1
        else:
            question_id_passed[row[3]] += 1
# 创建新的csv文件
fp = open('q4Out.csv',mode='w',encoding='utf-8-sig',newline="")
csv_write = csv.writer(fp)
csv_write.writerow(['Question ID', 'StudentsPassed'])
for key,value in question_id_passed.items():
    csv_write.writerow([key,value])
fp.close()