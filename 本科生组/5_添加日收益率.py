"""
    数据时间段是2019年01月29日—2020年03月26日
    数据包含Open（开盘价）、Close（收盘价）、High（最高价）、Turnover（成交额度）、Low（最低价）
    多因子模型的构建是基于丰富的数据供应基础上，在目前的这个比赛中，是不具备这个条件，所以只用5个基本特征数据加一个收益率的衍生变量
"""
# 先计算[日收益率],参考文章：https://blog.csdn.net/asialee_bird/article/details/89340563
import os
import csv
path = 'csv添加日收益率'
if not os.path.exists(path):
    os.mkdir(path)

files = os.listdir('csv数据集')
for file in files:
    Date = [row[0] for row in csv.reader(open('csv数据集' + '/' + file, mode="r", encoding="utf-8"))]
    Open = [row[1] for row in csv.reader(open('csv数据集' + '/' + file, mode="r", encoding="utf-8"))]
    High = [row[2] for row in csv.reader(open('csv数据集' + '/' + file, mode="r", encoding="utf-8"))]
    Low = [row[3] for row in csv.reader(open('csv数据集' + '/' + file, mode="r", encoding="utf-8"))]
    Close = [row[4] for row in csv.reader(open('csv数据集' + '/' + file, mode="r", encoding="utf-8"))]
    Turnover = [row[5] for row in csv.reader(open('csv数据集' + '/' + file, mode="r", encoding="utf-8"))]
    f = open(path + '/' + file, mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Turnover', '日收益率'])
    for i in range(1,len(Date)):
        if i == 1:
            csv_write.writerow([str(Date[i]).strip(),Open[i],High[i],Low[i],Close[i],Turnover[i],"NAN"])
        else:
            csv_write.writerow([str(Date[i]).strip(), Open[i], High[i], Low[i], Close[i], Turnover[i], (float(Close[i])-float(Close[i-1]))/(float(Close[i-1]))])
    f.close()

