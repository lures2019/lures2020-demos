"""
    获取用户输入月份，输出该月有多少天（考虑闰年）
"""
# 用户输入年份，以判定是否是闰年
year = int(input("请输入年份："))
month = int(input("请输入月份："))
# 判断闰年的条件如下
if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
    months = [31,29,31,30,31,30,31,31,30,31,30,31]
    print("该月有{}天".format(months[month-1]))
else:
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    print("该月有{}天".format(months[month - 1]))
