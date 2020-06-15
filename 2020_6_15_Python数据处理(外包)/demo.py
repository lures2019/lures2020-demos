"""
    1、使用pandas完成1~4题
    2、要求使用的第三方包：读取excel：xlrd/数据可视化：matplotlib
    任务一、风电场运行情况统计分析
    附件一给出了风电场一年内每隔15分中的各风机安装处的平均风速和风电场的日实际输出功率
"""

import xlrd
import xlwt
# Excel文件过多，导入os模块方便查看
import os
import matplotlib.pyplot as plt

# 问题数据文件
f = open("问题数据文件.txt",mode="w+",encoding="utf-8")
f.write("Excel文件名称"+"\t\t"+"时间"+"\t\t"+"功率"+"\t\t"+"风速"+"\n")
f.close()

# 处理后的数据集
path = '处理后数据集'
# 没有此目录则创建此目录
if not os.path.exists(path):
    os.mkdir(path)


# Step1、找出问题数据
"""
    1.	请问任务提供的数据中存在哪些问题？请对找出这些问题数据并以附件的形式提交，并采取适当地方式处理这些问题数据。
        （提示：正常情况下最高风速为32，最大功率不超过160。）
    2.  处理思路：使用python的xlrd模块依次读取附件1所示的各excel文件的各数据表
        将问题数据 所在的excel名称及数据表名称+问题数据写到txt文件中
    3.  对问题数据的处理：对于出现问题数据，暂时就先赋予最高值吧！(感觉应该和附件二和三有关)
"""
def according_wind_speed(x):
    # 以列表的形式呈现出所有的Excel文件
    xls_tables = os.listdir('附件1  平均风速和风电场日实际输出功率表')
    hours = 0
    speed = x
    # 统计每月的电场平均风速和平均速率的分布情况
    months_winds = []
    months_powers = []
    # 统计每天的电场平均风速和平均速率的分布情况
    days_winds = []
    days_powers = []

    for name in xls_tables:
        # 月风速和功率统计
        months_wind = 0
        months_power = 0
        days = 0

        xls_table = xlrd.open_workbook('附件1  平均风速和风电场日实际输出功率表/{}'.format(name))
        # 以列表的形式呈现出返回的xls文件的所有表名
        table_names = xls_table.sheet_names()
        # 创建workbook对象
        workbook = xlwt.Workbook(encoding='utf-8')
        for table_name in table_names:
            day_power = 0
            day_wind = 0
            # 根据表的名称获取表的对象
            sheet = xls_table.sheet_by_name(table_name)
            # 创建工作表worksheet
            worksheet = workbook.add_sheet(table_name)
            # 获取当前表的总行数，利用循环可以得到每一行的数据
            rows = sheet.nrows
            for i in range(3, rows):
                # 打印的是每一行的数据,功率所在的列是：1/4/7/10,风速所在的列是：2/5/8/11，时间所在的列是：0/3/6/9
                values_list = sheet.row_values(i)
                # print(sheet.row_values(i))
                for j in [1, 4, 7, 10]:
                    """
                        下面是有异常数据的数据表：
                            201503.xls-Sheet15
                            201503.xls-Sheet18
                            201507.xls-Sheet27
                            201507.xls-Sheet28
                            201507.xls-Sheet29
                            201509.xls-Sheet27
                            201503.xls-Sheet30          空格
                    """
                    values_now = ['4.4', '4.7', '5.2', '10.4', '3.1', '8.3', '0']
                    num = 0
                    if values_list[j + 1] in ['4..4', '4.74.9', '5.16.4', '10..4', '3..1', '8..3', '']:
                        with open("问题数据文件.txt", mode="a+", encoding="utf-8") as f:
                            f.write(name + '\t' + table_name + '\t\t' + str(values_list[j - 1]) + '\t\t' + str(
                                values_list[j]) + '\t\t' + values_list[j + 1] + "\n")
                        f.close()
                        months_wind += float(values_now[num])
                        day_wind += float(values_now[num])
                        months_power += float(values_list[j])
                        day_power += float(values_list[j])
                        # 如果满足大于6m/s的条件，就增加0.25h
                        if (float(values_now[num]) > speed):
                            hours += 0.25
                        worksheet.write(i, j - 1, values_list[j - 1])
                        worksheet.write(i, j, values_list[j])
                        worksheet.write(i, j + 1, values_now[num])
                        num += 1
                    elif (float(values_list[j]) > 160) or (float(values_list[j + 1]) > 32):
                        with open("问题数据文件.txt", mode="a+", encoding="utf-8") as f:
                            f.write(name + '\t' + table_name + '\t\t' + str(values_list[j - 1]) + '\t\t' + str(
                                values_list[j]) + '\t\t' + str(values_list[j + 1]) + '\n')
                        f.close()
                        if (float(values_list[j + 1]) > speed):
                            hours += 0.25
                        if (float(values_list[j]) > 160):
                            months_power += 160
                            day_power += 160
                            months_wind += float(values_list[j + 1])
                            day_wind += float(values_list[j + 1])
                            worksheet.write(i, j - 1, values_list[j - 1])
                            worksheet.write(i, j, 160)
                            worksheet.write(i, j + 1, values_list[j + 1])
                        else:
                            worksheet.write(i, j - 1, values_list[j - 1])
                            worksheet.write(i, j, values_list[j])
                            months_wind += 32
                            day_wind += 32
                            months_power += float(values_list[j])
                            day_power += float(values_list[j])
                            worksheet.write(i, j + 1, 32)
                    else:
                        if (float(values_list[j + 1]) > speed):
                            hours += 0.25
                        worksheet.write(i, j - 1, values_list[j - 1])
                        worksheet.write(i, j, values_list[j])
                        worksheet.write(i, j + 1, values_list[j + 1])
                        months_power += float(values_list[j])
                        day_power += float(values_list[j])
                        months_wind += float(values_list[j + 1])
                        day_wind += float(values_list[j + 1])
            days_powers.append(day_power)
            days_winds.append(day_wind)
        workbook.save(path + '/' + name)
        months_winds.append(months_wind)
        months_powers.append(months_power)
    if(speed == 6):
        return(hours,days_winds,days_powers,months_winds,months_powers)
    else:
        return(hours)


# Step2、
"""
    1.	请问全年各分场风速超过6 m/s的总小时数有多少？全年的平均风速和平均功率是多少？
        请分别以天、月为单位统计风电场平均风速和平均功率的分布情况？
        根据分布情况请尝试分析以天为单位的平均风速和平均功率之间存在怎样关系？
"""


# Step3、将第二问中的以天、月为单位统计的电场平均风速和平均功率的分布情况进行可视化
hours,days_winds,days_powers,months_winds,months_powers = according_wind_speed(6)
print("全年各分场风速超过6m/s的总小时数有{}h".format(hours))
x1 = range(0, 365)
plt.plot(x1, days_powers, label='按天分布的功率折线图')
plt.xlabel('days')
plt.ylabel('powers')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('days_powers')
plt.legend()
plt.savefig(path + '/' + 'days_powers.png')
plt.show()
plt.plot(x1, days_winds, label='按天分布的风速折线图')
plt.xlabel('days')
plt.ylabel('winds')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('days_winds')
plt.legend()
plt.savefig(path + '/' + 'days_winds.png')
plt.show()

x2 = range(1, 13)
plt.plot(x2, months_powers, label='按月分布的功率折线图')
plt.xlabel('months')
plt.ylabel('powers')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('months_powers')
plt.legend()
plt.savefig(path + '/' + 'months_powers.png')
plt.show()
plt.plot(x2, months_winds, label='按月分布的风速折线图')
plt.xlabel('months')
plt.ylabel('winds')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('months_winds')
plt.legend()
plt.savefig(path + '/' + 'months_winds.png')
plt.show()

hours_new = []
for x in [3,4,5,6,7,8,9,10]:
    if (x == 6):
        hours_new.append(hours)
    else:
        hours_new.append(according_wind_speed(x))
x3 = range(3, 11)
plt.plot(x3, hours_new, label='全年各分场风速折线图')
plt.xlabel('wind_speed')
plt.ylabel('hours')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('wind_speed_hours')
plt.legend()
plt.savefig(path + '/' + 'wind_speed_hours.png')
plt.show()


# Step4、请尝试利用提供的数据对该风电场的风能资源及其利用情况进行评估。
