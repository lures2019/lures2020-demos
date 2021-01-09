"""
    输入案例：
        40 50 60 70 80 100 160
"""
# 输入一周七天的AQI值（整数）
i = 1
# 创建星期字典
week_dict = {
    1:"周一",
    2:"周二",
    3:"周三",
    4:"周四",
    5:"周五",
    6:"周六",
    7:"周日"
}
while i <= 7:
    AQI = int(input("请输入当天的空气品质AQI值："))
    if AQI < 50:
        print("{}{}".format(week_dict[i],"空气良好"))
    elif AQI < 100:
        print("{}{}".format(week_dict[i], "空气普通"))
    elif AQI < 150:
        print("{}{}".format(week_dict[i], "敏感族不适合"))
    else:
        print("{}{}".format(week_dict[i], "全部族群不适合"))
    i += 1
