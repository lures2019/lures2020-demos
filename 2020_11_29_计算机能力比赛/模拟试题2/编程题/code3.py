"""
    输入一串字符，由字母、数字和空格组成，长度<1000，判断其中是否存在日期格式的数据。日期格式的数据具有如下特征，连续
        包含年份和月份信息。年份信息是指连续的四个数字，之后就是Jan、Feb、Mar、Apr、May、Jun、Jul、Aug、Sep、Oct、Nov、Dec
        这些字符串之一，如"2019Nov"就是符合日期格式要求的数据！
    输入说明：输入一个字符串
    输出说明：输出包含满足日期格式的字符子串，如果不包含，则输出2000Jan
    输入样例1：Todayis2019Nov15th
    输出样例1：2019Nov
    输入样例2：Todayisasunnyday
    输出样例2：2000Jan
    输入样例3：OnNov05,nothing happen
    输出样例3：2000Jan
"""
string = input()
EOF = -1
# 年份未设置一个范围，那四位数范围0000~9999，正好10000个
for i in range(10000):
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    dates = ["{:0>4d}".format(i) + month for month in months]
    for date in dates:
        if date in string:
            print(date)
            EOF = 1
            break
if EOF == -1:
    print("2000Jan")
