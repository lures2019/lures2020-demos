# 分析评论日期
import re
import matplotlib.pyplot as plt
import os
import datetime

# 对日期进行排序
def get_list(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()

# 首先获取json文件的所有短评信息
def get_datas_from_json():
    f = open('《安家》短评.json',mode='r',encoding='utf-8')
    datas = f.read()
    comments = re.findall("time\": (.*?)\n",datas)
    my_list = []
    for comment in comments:
        my_list.append(eval(comment))
    return my_list

# 存储评论日期（2020年2月到3月期间
def get_effective_datas():
    my_list = get_datas_from_json()
    new_list = []
    # 进行遍历筛选
    for date in my_list:
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        if year > 2019 and month > 1 and month < 4:
            new_list.append(date)
    # 使用字典进行数据的统计
    my_dict = {}
    new_list = sorted(new_list,key=lambda date:get_list(date))
    for date in new_list:
        if date not in my_dict:
            my_dict[date] = 1
        else:
            my_dict[date] += 1
    # 分键值存放对应列表
    keys = list(my_dict.keys())
    values = list(my_dict.values())
    return keys,values

# 使用matplotlib开始绘图
def draw_line_chart(path):
    keys,values = get_effective_datas()
    # 创建一个画布，指定宽、高
    plt.figure(figsize=(20, 10))
    # 设置显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 绘制折线图
    plt.plot(keys, values, marker='o')
    # 这里是调节坐标的倾斜度，rotation是度数，以及设置刻度字体大小
    plt.xticks(keys, rotation=45, fontsize=15)
    plt.yticks(fontsize=15)
    # 配置坐标标题
    plt.xlabel("发布日期", fontsize=15)
    plt.ylabel("评论数量", fontsize=15)
    # 网格化
    plt.grid()
    # 保存图形
    plt.savefig(path + '/' + '《安家》评论趋势折线图.jpg')
    # 显示图形
    plt.show()


if __name__ == "__main__":
    path = "pictures"
    # 不存在此目录则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    draw_line_chart(path)
