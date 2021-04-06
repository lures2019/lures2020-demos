import os
import pandas as pd
import matplotlib.pyplot as plt

dst_path = '../datasets/archive/US'
names = os.listdir(dst_path)
# 创建大列表，分别统计视频名称以及统计次数
videos_name = []
videos_count = []
for i in range(4):
    my_df = pd.read_csv('../datasets/archive/US/USvideos_out{}.csv'.format(i), index_col='video_id')
    cdf = my_df.groupby("channel_title").size().reset_index(name="video_count") \
        .sort_values("video_count", ascending=False).head(100)
    videos_name.append(list(cdf.channel_title))
    videos_count.append(list(cdf.video_count))
# 使用字典将所有的视频存储——默认是数据中心
my_dict = {}
for i in range(3):
    for j in range(len(videos_name[i])):
        if videos_name[i][j] not in my_dict:
            my_dict[videos_name[i][j]] = videos_count[i][j]
        else:
            my_dict[videos_name[i][j]] += videos_count[i][j]
# 说明有125个类重叠了,175就是数据中心的
print(len(my_dict))
# 下面需要求出每两个基站之间的共享缓存区和私有缓存区之间的视频内容
"""
    基站1:
        基站1和基站2之间的共享缓存区，基站1和基站3之间的共享缓存区，基站1独自的私有缓存区
    基站2:
        基站2和基站1之间的共享缓存区，基站2和基站3之间的共享缓存区，基站2独自的私有缓存区
    基站1:
        基站3和基站1之间的共享缓存区，基站3和基站2之间的共享缓存区，基站3独自的私有缓存区
"""
# 创建一个函数，用于调用求其平均时间
def function(dst,list1,list2,list3,t1,t2,t3,T):
    # 其中dst表示测试数据集，list1~list3分别代表基站1~3，dst在它们中间找不到数则认为是在数据中心
    # 求出三个基站共有的内容
    area = []
    for i in list1:
        if i in list2 and i in list3:
            area.append(i)
    # 求出两个基站共有的
    area12 = []
    area13 = []
    area23 = []
    # 基站私有
    area1 = []
    area2 = []
    area3 = []
    # 在基站1
    for i in list1:
        if i in list2:
            area12.append(i)
        elif i in list3:
            area13.append(i)
        else:
            area1.append(i)
    # 在基站2
    for i in list2:
        if i in list1:
            pass
        elif i in list3:
            area23.append(i)
        else:
            area2.append(i)
    # 在基站3
    for i in list3:
        if i in list1:
            pass
        elif i in list2:
            pass
        else:
            area3.append(i)
    # 开始遍历，计算时间
    total = 0
    if dst != 0:
        for i in dst:
            if i in area:
                total += t1
            elif i in area12 or i in area13 or i in area23:
                total += (t1 + t2)
            elif i in area1 or i in area2 or i in area3:
                total += (t1 + t2 + t3)
            else:
                total += T
        # 返回总时间和平均值
        return total, total / len(dst)
    else:
        return total,total


# 现在求传统缓存策略需要的总时间
def fun2(dst,list1,list2,list3,t3,T1):
    total = 0
    if dst != 0:
        for i in dst:
            if i in list1 or i in list2 or i in list3:
                total += t3
            else:
                total += T1
    return total


# 进行测试
list1 = videos_name[0]
list2 = videos_name[1]
list3 = videos_name[2]
t1 = 0.01
t2 = 0.02
t3 = 0.03
T = 0.05
T1 = 0.06

# 更改测试用户的数目
dst = videos_name[3]
# 最大测试用户100个
dsts = [0,dst[:20],dst[:40],dst[:60],dst[:80],dst]
users = [0,20,40,60,80,100]
# 存储总时间和平均时间
totals = []
average = []
tra_total = []
for i in range(len(dsts)):
    x = function(dsts[i], list1, list2, list3, t1, t2, t3, T)[0]
    y = function(dsts[i], list1, list2, list3, t1, t2, t3, T)[1]
    k = fun2(dsts[i],list1,list2,list3,t3,T1)
    # 保留1位小数
    totals.append(round(x*1000,1))
    average.append(round(y*1000,1))
    tra_total.append(round(k*1000,1))
    print("{}个用户测试总时间是：{:.1f} ms".format(users[i],x*1000))
print(totals,average)

# 绘出平均值的折线图
path = "pictures"
# 创建文件夹用于存储图
if not os.path.exists(path):
    os.mkdir(path)
plt.plot(users, average, label='平均延迟', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.xlabel('用户数')
plt.ylabel('平均延迟/ms')
plt.title('簇内共享缓存策略用户平均延迟折线图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.savefig(path + '/' + '簇内共享缓存策略用户平均延迟折线图.png')
plt.show()


# 开始绘制两者比较的折线图
plt.plot(users, tra_total, label='传统缓存策略', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.plot(users, totals, label='簇内共享缓存策略')
plt.xlabel('用户数')
plt.ylabel('总延迟/ms')
plt.title('折线对比图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.savefig(path + '/' + '折线对比图.jpg')
plt.show()