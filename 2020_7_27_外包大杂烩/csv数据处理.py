"""
    处理要求：
        对于每一列，从第一个有数据的行开始往下寻找，如果有数据缺失，就用同一列上一行的数据进行补充
        大致看了下数据：
            1）有些数据是前面的几列是空的，但是后面的是有数据的，这样的话保留原格式就好
            2）一列起始是有数据的，但是在中间有部分数据是缺失的，这时候就需要用到上一行数据进行补充
"""
import csv

f = open('deposit.csv',mode='r',encoding='utf-8')
rows = [row for row in csv.reader(f)]
# 得到此csv文件的总列数，依次进行遍历
# 创建新的csv文件进行保存处理后的csv数据
file = open('new_data.csv',mode='a+',encoding='utf-8',newline='')
csv_write = csv.writer(file)

start_data = rows[1]
datas = [[] for i in range(len(rows[0]))]
for i in range(len(rows[0])):
    with open('deposit.csv',mode='r',encoding='utf-8') as fp:
        column = [row[i] for row in csv.reader(fp)]
    for j in range(2,len(column)):
        # 第二行数据开始判断，如果第二行数据中有空的，就用start_data中对应列的数据
        if(j == 2 and column[j].strip() == ''):
            column[j] = start_data[i]
        elif(column[j].strip() == ''):
            column[j] = column[j-1]
        else:
            pass
    datas[i].append(column)
for i in range(4372):
    line_data = []
    for data in datas:
        line_data.append(data[0][i])
    csv_write.writerow(line_data)

file.close()