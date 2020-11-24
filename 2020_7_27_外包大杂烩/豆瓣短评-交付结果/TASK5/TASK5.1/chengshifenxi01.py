import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mp1

# 设置标签
# x =["北京","山西","上海","广东","郑州","天津"]
x = ["0-2", "2.1-4", "4.1-6", "6.1-8", "8.1-10", "10-"]

# 设置数据
# y1 = [9.2, 6.8, 9.8, 8.6, 5.9, 7.8]
y1 = [300, 3089, 2068, 1069, 206, 28]

mp1.rcParams['font.family'] = 'STFangsong'
plt.bar(x, y1, label="数量", color='orange')
plt.xticks(np.arange(len(x)), x, rotation=0, fontsize=10)  # 数量多可以采用270度，数量少可以采用340度，得到更好的视图
plt.legend(loc="upper left")  # 防止label和图像重合显示不出来
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.ylabel('会龄')
plt.xlabel('数量')
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
plt.title("用户的会龄分布")
# plt.savefig('D:\\result.png')
plt.show()
