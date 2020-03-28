import matplotlib.pyplot as plt
import os

path = '新增折线图'
if not os.path.exists(path):
    os.mkdir(path)
# 第一部分数据：境外输入+国家增长
dates1 = ['3月3号','3月4号','3月9号','3月14号','3月19号','3月23号']
overseas_input = [0,2,2,16,39,74]
national_growth = [120,143,20,27,65,147]
# Python画折线图
# Python画境外输入和国家增长折线图
plt.plot(dates1, national_growth, label='国家增长', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.plot(dates1, overseas_input, label='境外输入')
plt.xlabel('日期')
plt.ylabel('新增人数')
plt.title('境外输入+国家增长折线图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.savefig(path + '/' + '境外输入_国家增长折线图.jpg')
plt.show()


# 第二部分数据：全国+湖北+非湖北+新增趋势+现有趋势+治愈趋势
dates2 = ['1月27号','2月4号','2月12号','2月17号','2月19号','2月28号','3月1号','3月18号']
# 新增数据
country_new_added = [769,3887,15153,1891,825,430,25,84]
hubei_new_added = [371,3156,14840,1807,775,423,8,0]
not_hubei_new_added = [398,731,313,84,50,7,17,84]
# Python画折线图
# Python画国家新增+湖北新增+非湖北新增折线图
plt.plot(dates2, country_new_added, label='国家新增', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.plot(dates2, hubei_new_added, label='湖北新增')
plt.plot(dates2, not_hubei_new_added, label='非湖北地区新增')
plt.xlabel('日期')
plt.ylabel('新增人数')
plt.title('国家新增+湖北新增+非湖北地区新增折线图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.savefig(path + '/' + '国家_湖北_非湖北新增折线图.jpg')
plt.show()


# 现有数据
country_now = [4369,22980,52599,58097,56810,37502,14920,7438]
hubei_now = [2567,15679,43455,50338,50091,34715,14427,6992]
not_hubei_now = [1802,7301,9144,7759,6719,2787,493,446]
# Python画折线图
# Python画国家新增+湖北新增+非湖北现有折线图
plt.plot(dates2, country_now, label='国家现有', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.plot(dates2, hubei_now, label='湖北现有')
plt.plot(dates2, not_hubei_now, label='非湖北现有')
plt.xlabel('日期')
plt.ylabel('现有人数')
plt.title('国家现有+湖北现有+非湖北地区现有折线图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.savefig(path + '/' + '国家_湖北_非湖北现有折线图.jpg')
plt.show()


# 治愈率
dates3 = ['1月27号','2月2号','3月5号','3月23号']
hubei_cure_rate = ['1.73%','2.64%','62.09%',' 88.97%']
not_hubei_cure_rate = ['0.71%','2.97%','90.16%','93.04%']
# Python画折线图
# Python画湖北+非湖北治愈率折线图
plt.plot(dates3, hubei_cure_rate, label='湖北治愈率', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.plot(dates3, not_hubei_cure_rate, label='非湖北地区治愈率')
plt.xlabel('日期')
plt.ylabel('治愈率')
plt.title('湖北+非湖北地区治愈率折线图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.legend()
plt.savefig(path + '/' + '湖北_非湖北治愈率折线图.jpg')
plt.show()

# 第三部分数据：国外总新增折线图
dates4 = ['2月22号','2月26号','3月2号','3月8号','3月14号','3月16号','3月21号']
new_abroad = [202,459,1600,3610,7488,13874,31884]
# Python画折线图
# Python画国外总新增折线图
plt.plot(dates4, new_abroad, label='国外总新增', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.xlabel('日期')
plt.ylabel('人数')
plt.title('国外总新增折线图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.savefig(path + '/' + '国外总新增折线图.jpg')
plt.show()


# 第四部分：国外国家折线图：累计确诊
dates5 = ['2月23号','3月1号','3月8号','3月16号','3月20号','3月23号']
countries = ['意大利','西班牙','德国','伊朗','美国']
Italy_total = [132,1128,7424,24727,41035,63927]
Spain_total = [2,45,430,9942,24926,35136]
Germany_total = [16,117,921,6012,18607,28729]
Iran_total = [43,978,6566,16169,20610,23094]
United_States_total = [34,69,445,4629,19624,46332]
# Python画折线图
# Python画意大利+西班牙+德国+伊朗+美国累计确诊折线图
plt.plot(dates5, Italy_total, label='意大利累计确诊', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
plt.plot(dates5, Spain_total, label='西班牙累计确诊')
plt.plot(dates5, Germany_total, label='德国累计确诊')
plt.plot(dates5, Iran_total, label='伊朗累计确诊')
plt.plot(dates5, United_States_total, label='美国累计确诊')
plt.xlabel('日期')
plt.ylabel('累计确诊人数')
plt.title('意大利+西班牙+德国+伊朗+美国累计确诊折线图')
# 显示中文名称
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.savefig(path + '/' + '意大利_西班牙_德国_伊朗_美国累计确诊折线图.jpg')
plt.show()

