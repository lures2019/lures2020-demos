"""
    要求：Python爬取国内疫情信息进行可视化展示
    思路：通过爬取网页——https://news.qq.com/zt2020/page/feiyan.htm#/?nojump=1
            来获取从第1例疫情开始出现到今天的所有的【每天新增】【现存】的情况
            最后通过这些数据进行可视化展现
"""

# 网页爬虫的基本库
import requests
# 文件操作的基本库
import os
# 可视化图形绘制库
import matplotlib.pyplot as plt
import numpy as np

path = '疫情图集'
if not os.path.exists(path):
    # 若没有此目录则创建一个
    os.mkdir(path)

def data_spyder(number):
    # 定义新变量，接收传进的参数
    num = number
    # 经过分析网页获取到的数据接口
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare'
    response = requests.get(url=url)
    # 万能解码，使中文不会以乱码的形式展现
    response.encoding = response.apparent_encoding
    # 接口的数据是json格式的
    html = response.json()
    """下面的代码是获取每天的新增的数目"""
    day_add_datas = html['data']['chinaDayAddList']
    # 使用列表的append方法将对应种类的新增数目添加到各自的列表中，以便于后面的可视化操作
    day_deads = []  # 新增死亡
    day_heals = []  # 新增治愈
    day_dates = []  # 日期
    day_confirms = []  # 新增确诊

    # 如果数据全部存在列表中，最后绘图时密密麻麻，于是隔20天写入一次
    for i in range(len(day_add_datas)):
        if (i % 20 == 0):
            day_deads.append(day_add_datas[i]['dead'])
            day_heals.append(day_add_datas[i]['heal'])
            day_confirms.append(day_add_datas[i]['confirm'])
            day_dates.append(day_add_datas[i]['date'])

    """下面的代码是获取当天的各种累计数目"""
    day_datas = html['data']['chinaDayList']
    # 同样的操作，将各种栏目的数据添加到对应的列表中
    deads = []
    heals = []
    dates = []
    confirms = []

    for i in range(len(day_datas)):
        if(i % 20 == 0):
            deads.append(day_datas[i]['dead'])
            heals.append(day_datas[i]['heal'])
            dates.append(day_datas[i]['date'])
            confirms.append(day_datas[i]['confirm'])

    # 现在是将上面的代码整体封装成一个函数，通过调用不同的参数获取不同的return返回对象
    if num == 1:
        # 如果num是1的话返回的是累计的数目
        return(dates,deads,heals,confirms)
    elif(num == 2):
        # 如果num是2的话返回的是每天的新增数目
        return(day_dates,day_deads,day_heals,day_confirms)
    else:
        print('传进的参数有问题，调用失败！')

# 绘制每天的数据图
def paint_day_chart():
    day_dates, day_deads, day_heals, day_confirms = data_spyder(2)
    titles = ['日期','新增死亡数','新增治愈数','新增确诊数']
    datas = [day_dates,day_deads,day_heals,day_confirms]
    for i in range(1,len(titles)):
        plt.plot(day_dates,datas[i],label="每日{}".format(titles[i]),linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=12)
        plt.xlabel('日期')
        plt.ylabel(titles[i])
        plt.title('每日{}'.format(titles[i]))
        # 使中文可以正常显示出来
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.legend()
        plt.savefig(path + '/' + titles[i] + '_折线图.jpg')
        plt.show()
        plt.figure()
        # 下面时绘制柱状图
        plt.bar(day_dates,datas[i])
        plt.xlabel('日期')
        plt.ylabel(titles[i])
        plt.title('每日{}'.format(titles[i]))
        # 使中文可以正常显示出来
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.savefig(path + '/' + titles[i] + '_柱状图.jpg')
        plt.show()


# 绘制累计的数据图
def paint_chart():
    dates, deads, heals, confirms = data_spyder(1)
    plt.plot(dates, deads, label='累计死亡数', linewidth=3, color='r', marker='o',markerfacecolor='blue', markersize=12)
    plt.xlabel('日期')
    plt.ylabel('累计死亡数')
    plt.title('累计死亡数折线图')
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path + '/' + '累计死亡数折线图.jpg')
    plt.show()
    plt.figure()
    # 下面绘制柱状图
    plt.bar(dates, deads)
    plt.xlabel('日期')
    plt.ylabel('累计死亡数')
    plt.title('累计死亡数柱状图')
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.savefig(path + '/'  + '累计死亡数柱状图.jpg')
    plt.show()
    plt.figure()

    # 下面是将累计治愈和累计确诊两条折现放在一个图中
    plt.plot(dates,heals,label="累计治愈数",linewidth=3,color='r', marker='o',markerfacecolor='blue', markersize=12)
    plt.plot(dates,confirms,label="累计确诊数")
    plt.xlabel('日期')
    plt.ylabel('患者人数')
    plt.title("累计治愈_确诊折线图")
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path + '/' + '累计治愈_确诊折线图.jpg')
    plt.show()
    plt.figure()

    # 下面绘制柱状图
    bar_width = 0.25
    x = np.arange(len(dates))
    plt.bar(x, heals, bar_width, align="center", color="red", label="累计治愈数", alpha=0.5)
    plt.bar(x + bar_width, confirms, bar_width, color="purple", align="center",label="累计确诊数", alpha=0.5)
    plt.xlabel('日期')
    plt.ylabel('患者人数')
    plt.title('累计治愈_确诊柱状图')
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(x + bar_width / 2, dates)
    plt.legend()
    plt.savefig(path + '/' + '累计治愈_确诊柱状图.jpg')
    plt.show()


# 爬取世界每日患者数据
# 经过分析页面找到了新的数据接口
def spyder_foreign_data():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoContinentStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd'
    response = requests.get(url=url)
    response.encoding = response.apparent_encoding
    datas = response.json()['data']['FAutoGlobalDailyList']
    world_dates = []
    world_heals = []
    world_confirms = []
    world_deads = []
    world_newAddConfirms = []
    for i in range(len(datas)):
        if (i % 20 == 0):
            world_dates.append(datas[i]['date'])
            world_confirms.append(datas[i]['all']['confirm'])
            world_deads.append(datas[i]['all']['dead'])
            world_heals.append(datas[i]['all']['heal'])
            world_newAddConfirms.append(datas[i]['all']['newAddConfirm'])
    return(world_dates,world_deads,world_heals,world_confirms,world_newAddConfirms)

def paint_chart_foreign():
    world_dates, world_deads, world_heals, world_confirms, world_newAddConfirms = spyder_foreign_data()
    datas = [world_dates, world_deads, world_heals, world_confirms, world_newAddConfirms]
    titles = ['日期','世界累计死亡数','世界累计治愈数','世界累计确诊数','世界每日新增确诊数']
    for i in range(1,len(datas)):
        plt.plot(datas[0], datas[i], label=titles[i], linewidth=3, color='r', marker='o', markerfacecolor='blue', markersize=12)
        plt.xlabel('日期')
        plt.ylabel(titles[i])
        plt.title('{}折线图'.format(titles[i]))
        # 使中文可以正常显示出来
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.legend()
        plt.savefig(path + '/' + titles[i]+'_折线图.jpg')
        plt.show()
        plt.figure()
        # 下面绘制柱状图
        plt.bar(datas[0], datas[i])
        plt.xlabel('日期')
        plt.ylabel(titles[i])
        plt.title('{}_柱状图'.format(titles[i]))
        # 使中文可以正常显示出来
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.savefig(path + '/' + titles[i]+'_柱状图.jpg')
        plt.show()
        plt.figure()


if __name__ == '__main__':
    paint_chart()
    paint_day_chart()
    paint_chart_foreign()