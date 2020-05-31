import csv
import os

files = os.listdir('csv数据集')
path = '处理后csv数据集'
if not os.path.exists(path):
    os.mkdir(path)
max_a = []
max_b = []
for file in files:
    Date = [row[0] for row in csv.reader(open('csv数据集' + '/' + file,mode="r",encoding="utf-8"))]
    Open = [row[1] for row in csv.reader(open('csv数据集' + '/' + file,mode="r",encoding="utf-8"))]
    High = [row[2] for row in csv.reader(open('csv数据集' + '/' + file,mode="r",encoding="utf-8"))]
    Low = [row[3] for row in csv.reader(open('csv数据集' + '/' + file,mode="r",encoding="utf-8"))]
    Close = [row[4] for row in csv.reader(open('csv数据集' + '/' + file,mode="r",encoding="utf-8"))]
    Turnover = [row[5] for row in csv.reader(open('csv数据集' + '/' + file,mode="r",encoding="utf-8"))]
    f = open(path + '/' + file,mode="a+",newline="",encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['Date','Open','High','Low','Close','Turnover','收盘-开盘(a)','最高-最低(b)'])
    sum_a = 0           # 求均值
    sum_b = 0
    variance_a = 0      # 求方差
    variance_b = 0
    for i in range(1,len(Date)-1):
        a = float(Close[i]) - float(Open[i])
        sum_a += a
        b = float(High[i]) - float(Low[i])
        sum_b += b
    for j in range(1,len(Date)-1):
        a = float(Close[j]) - float(Open[j])
        b = float(High[j]) - float(Low[j])
        variance_a += ((a-sum_a/280)**2)
        variance_b += ((b-sum_b/280)**2)
    for k in range(1,len(Date)):
        a = float(Close[k]) - float(Open[k])
        b = float(High[k]) - float(Low[k])
        csv_write.writerow([Date[k],Open[k],High[k],Low[k],Close[k],Turnover[k],a,b])

    csv_write.writerow('\n')
    csv_write.writerow(['a的均值','a的方差','a(均值/方差)','b的均值','b的方差','b(均值/方差)'])
    max_a.append(sum_a/variance_a)
    max_b.append(sum_b/variance_b)
    csv_write.writerow([sum_a/279,variance_a/279,sum_a/variance_a,sum_b/279,variance_b/279,sum_b/variance_b])
    f.close()

# 给10支股票打分
fp = open(path + '/'+'10支股票打分情况.txt',mode="w",encoding='utf-8')
fp.write("10支股票（均值/方差）最大值："+"\n")
fp.write("\t"+"①收益(a)最高分："+"\n")
fp.write("\t"+str(max(max_a)) + "\n")
fp.write("\t"+"②风险(b)最高分："+"\n")
fp.write("\t"+str(max(max_b)) + "\n")
fp.write("*"*100+"\n")
fp.write("10支股票（均值/方差）所有数值："+"\n")
fp.write("\t"+"①收益(a)数值情况："+"\n")
fp.write("\t"+str(max_a) + "\n")
fp.write("\t"+"②风险(b)数值情况："+"\n")
fp.write("\t"+str(max_b) + "\n")
fp.write("*"*100+"\n")
fp.write("下面是收益(a)相对最高分时的打分情况"+"\n")
sum_a_average = 0
sum_b_average = 0
for i in range(len(max_a)):
    fp.write("\t"+files[i].replace(r'.csv','')+":"+"\t"+str((max_a[i]/max(max_a))*100)+"\n")
    sum_a_average += (max_a[i]/max(max_a))*100
fp.write("\t"+"收益打分平均值："+"\t"+str(sum_a_average/10)+"\n")
fp.write("*"*100+"\n")
fp.write("下面是风险(b)相对最高分时的打分情况"+"\n")
for i in range(len(max_b)):
    fp.write("\t"+files[i].replace(r'.csv','')+":"+"\t"+str((max_b[i]/max(max_b))*100)+"\n")
    sum_b_average += (max_b[i]/max(max_b))*100
fp.write("\t"+"风险打分平均值："+"\t"+str(sum_b_average/10)+"\n")