"""
    title:新冠疫情数据分析与可视化
    time:2020/6/18
    大致思路：使用爬虫的基本库requests爬取腾讯新闻的数据，保存到csv文件中，再使用可视化的基本库matplotlib和
            画疫情数据的折线图
            因为这边得到的国家全是中文，因此无法用pyecharts画出世界地图
"""
import requests
import csv
import os
import matplotlib.pyplot as plt
import time

# Step1、国外疫情数据爬取
"""
    参考博客：https://blog.csdn.net/qq_46614154/article/details/105634848
    找到了国外疫情数据的post接口：
        https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E7%BE%8E%E5%9B%BD&
        %E7%BE%8E%E5%9B%BD这里代表的是美国
        可以将我们想爬取的国家信息替换美国，得到我们的相应的国家命名的csv文件
"""
# 创建一个目录，专门用来存储国外的疫情数据csv文件
path = '国外疫情数据'
# 没有此目录则创建此目录
if not os.path.exists(path):
    os.mkdir(path)

def get_foreign_messages(country):
    country = country
    # 单独创建每个国家的文件夹
    path_now = path + '/' + country
    # 没有此文件夹则创建此文件夹
    if not os.path.exists(path_now):
        os.mkdir(path_now)
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={}&'.format(country)
    # 这里面设置的便是一些常见的反爬参数
    headers = {
        'Host': 'api.inews.qq.com',
        'Origin': 'https://news.qq.com',
        'Referer': 'https://news.qq.com/zt2020/page/feiyan.htm',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.post(url=url, headers=headers)
    # 设置编码格式————万能解码
    response.encoding = response.apparent_encoding
    """
        # 打印出我们需要的参数的列表
        print(response.json()['data'])
        # 查看我们得到的数据的长度
        print(len(response.json()['data']))
    """
    datas = response.json()['data']
    # 创建csv文件，存储疫情数据文件
    # 其中mode="w"表示写的方式,newline=""表示不换行，encoding="utf-8-sig"设置编码格式，免得打开csv文件时出现乱码
    f = open(path_now + '/' + '{}疫情历史数据.csv'.format(country), mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['日期', '新增确诊', '确诊总数', '治愈数', '死亡数'])
    f.close()
    # 以上都是为了csv文件格式好看
    # 现在开始将json文件提取得到的数据写入到刚才创建的csv文件中并将几个重要的数据写进列表中，方便后面的可视化操作
    dates = []  # 日期列表
    confirm_add = []  # 新增确诊
    confirm = []  # 累计确诊
    heal = []  # 治愈
    dead = []  # 死亡

    with open(path_now + '/' + "{}疫情历史数据.csv".format(country), mode="a+", newline="", encoding="utf-8-sig") as f:
        csv_write = csv.writer(f)
        # 直接列表存储的话，后面画图很密集，这边打算15个数据中显示一个
        num = 1
        for data in datas:
            csv_write.writerow([data['date'], data['confirm_add'], data['confirm'], data['heal'], data['dead']])
            if (num % 15 == 0):
                dates.append(data['date'])
                confirm_add.append(data['confirm_add'])
                confirm.append(data['confirm'])
                heal.append(data['heal'])
                dead.append(data['dead'])
            else:
                pass
            num += 1
    f.close()
    # 返回一些参数，为后续的画图提供数据
    return(dates,confirm,heal,confirm_add,dead,path_now)


# Step2、上面的代码已经实现将查询国家的历史疫情数据爬取到csv文件中，下面根据上面爬虫程序返回的各列数据的列表画折线图
# 数量级差不多的两个参数放一块dead和confirm_add/confirm和heal
def draw_add_dead_pictures(country):
    country = country
    dates, confirm, heal, confirm_add, dead,path_now = get_foreign_messages(country)
    plt.plot(dates, confirm_add, label='新增确诊', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(dates, dead, label='死亡')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('疫情历史数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path_now + '/' + '{}新增确诊_死亡病例折线图.jpg'.format(country))
    plt.show()


def draw_confirm_heal_pictures(country):
    country = country
    dates, confirm, heal, confirm_add, dead,path_now = get_foreign_messages(country)
    plt.plot(dates, confirm, label='确诊', linewidth=3, color='r', marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, heal, label='死亡')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('疫情历史数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path_now + '/' + '{}确诊_治愈病例折线图.jpg'.format(country))
    plt.show()

# 做完以上的内容后，现在开始封装函数，传入的参数就是国家的名称
# 现在开始显示所有的国家列表
# 经分析，找到了海外国家的接口信息：https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist
def get_foreign_country():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    # 一些反爬参数
    headers = {
        'Host': 'api.inews.qq.com',
        'Origin': 'https://news.qq.com',
        'Referer': 'https://news.qq.com/zt2020/page/feiyan.htm',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.post(url=url, headers=headers)
    # 设置编码，以实现万能解码
    response.encoding = response.apparent_encoding
    """
        # 显示包含国家数据在内的列表
        print(response.json()['data'])
        # 显示列表的长度，方便提取到国家的名字
        print(len(response.json()['data']))
    """
    datas = response.json()['data']
    # 创建空列表，存储国家信息
    countrys = []
    for data in datas:
        countrys.append(data['name'])
    return (countrys)

if __name__ == '__main__':
    # 这边运行的是国外的疫情爬虫程序
    countrys = get_foreign_country()
    for country in countrys:
        get_foreign_messages(country)
        draw_add_dead_pictures(country)
        draw_confirm_heal_pictures(country)
        print("{}疫情历史数据已经抓取，并存放到{}疫情历史数据.csv文件中".format(country, country))
        # 每抓取一次，休眠2s，防止ip被封
        time.sleep(2)
    print("所有国家的信息都提取完毕!")


