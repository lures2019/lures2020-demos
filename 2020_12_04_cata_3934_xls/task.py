"""
    任务一：
        两张表中的 企业加起来接近6000条，调用高德API进行地理位置逆编码的时候，大概跑一次下次就要重新换一个API
        将经纬度坐标找到之后保存在别的csv文件中
        调用高德web框架展示这些坐标信息
    任务二：
        统计各个站点的比例，画饼状图
    任务三：
        找到带永嘉的公司，统计下种类占比，绘制一下柱状图
"""
import xlrd
import os
import csv
import requests
import matplotlib.pyplot as plt

path = '处理后csv文件'
if not os.path.exists(path):
    # 不存在此目录则创建一个这样的文件夹
    os.mkdir(path)


# 1、先将xls格式的文件转换为对应的csv文件，不但可以变小，也方便后续操作
def change_xls_to_csv():
    filenames = ['cata_3934_1.xls','cata_3934_2.xls']
    for file in filenames:
        # 注意csv文件创建时必须确定编码格式是utf-8-sig，否则打开时乱码，另外newline=""的作用是不换行
        file_now = file.split('.xls')[0]
        f = open(path + '/' + "{}.csv".format(file_now), mode='w', encoding='utf-8-sig', newline="")
        csv_write = csv.writer(f)

        # 使用xlrd模块读取xls格式文件
        wb = xlrd.open_workbook(file)
        # 打开excel文件的sheet表,只有['Sheet1']
        sheet_names = wb.sheet_names()
        # 选中默认的sheet表进行操作
        work_sheet = wb.sheet_by_name('Sheet1')
        # 统计sheet的行数和列数，因为xls格式是读取单元格的值,下面分别是读取行数和列数
        nrows = work_sheet.nrows
        ncols = work_sheet.ncols
        # xlrd可以按行读取，不像openpyxl是按照单元格进行读取的
        for i in range(nrows):
            csv_write.writerow(work_sheet.row_values(i))
        # 关闭文件
        f.close()

# 2、从转换后的csv文件中提取需要的信息组建新的csv文件，即文件中的E/F/H三列，合并成一个csv文件
def get_effective_information():
    # 首先是读取csv文件
    filenames = ['cata_3934_1.csv','cata_3934_2.csv']
    # 准备存放的csv文件集合,写入的模式不能用"a+"，否则会多次写入造成雍冗
    fp = open(path + '/' + '合并未转换经纬度.csv',mode='w+',encoding='utf-8-sig',newline="")
    csv_write = csv.writer(fp)
    # 不准备将标题也代入新的csv文件
    for file in filenames:
        f = open(path + '/' + file,mode='r',encoding='utf-8-sig')
        csv_reader = csv.reader(f)
        rows = [i for i in csv_reader]
        new_rows = [[] for i in range(len(rows)-1)]
        for i in range(1,len(rows)):
            new_rows[i-1].append(rows[i][4])
            new_rows[i-1].append(rows[i][5])
            new_rows[i-1].append(rows[i][7])
        for row in new_rows:
            csv_write.writerow(row)
    fp.close()


# 3、调用高德API，将经纬度信息写入csv文件中，注意高德API的调用次数在300000次左右
# 意思是这个代码每运行50次，高德API都要更换一次,建议这个函数不要经常执行，因为等待时间比较久
def get_latitude_and_longitude_by_location():
    """开发文档：https://lbs.amap.com/api/webservice/guide/api/georegeo/"""
    # 创建测试地址数据集
    locationList = []
    f = open(path + '/' + '合并未转换经纬度.csv', mode='r', encoding='utf-8-sig')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    for row in rows:
        str_now = row[2]
        locationList.append(str_now)
    # 进行地理编码,执行时间有点长，耐心等待——因为是爬虫操作
    for i in range(len(locationList)):
        url = 'https://restapi.amap.com/v3/geocode/geo?address={}&output=json&key=ad8d7c6788d76913dc8f87a0460b7214'.format(locationList[i])
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        # 打印序数，免得无聊
        print(i)
        # 有些位置通过高德并没有展示出来，需要异常处理
        try:
            location = response.json()['geocodes']
            # 获取不到对应的编码的情况
            if len(location) == 0:
                rows[i].append("")
                rows[i].append("")
                rows[i].append("")
            else:
                data = location[0]['location']
                # 将具体的市信息写入csv文件
                location_now = location[0]['formatted_address']
                rows[i].append(location_now)
                # 将经纬度信息存储进去
                rows[i].append(data.split(',')[0])
                rows[i].append(data.split(',')[1])
        # 此处是一些莫名其妙的问题
        except Exception as error:
            rows[i].append("")
            rows[i].append("")
            rows[i].append("")
            print(error)
    fp = open(path + '/' + '添加经纬度后csv文件.csv', mode='a+', encoding='utf-8-sig', newline="")
    csv_write = csv.writer(fp)
    csv_write.writerow(rows[0])
    for row in rows:
        csv_write.writerow(row)
    fp.close()

# 4、删除那些地理逆编码失败的行，存放到新csv文件
def delete_useless_row():
    f = open(path + '/' + '添加经纬度后csv文件.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    new_rows = []
    for row in rows:
        # 删除row[-1]长度是0的数据所在的行
        if len(row[-1]) == 0:
            pass
        else:
            value = "{},{}".format(row[3],row[4])
            new_row = [row[0],row[1],row[2],value]
            new_rows.append(new_row)
    fp = open(path + '/' + '处理添加经纬度后csv文件.csv',mode='w+',encoding='utf-8-sig',newline="")
    csv_write = csv.writer(fp)
    csv_write.writerow(["所属行业","站点名称","企业名称","经纬度"])
    for row in new_rows:
        csv_write.writerow(row)
    fp.close()


# 5、统计各个站点的比例，画一下饼状图
def paint_pie_picture():
    f = open(path + '/' + '处理添加经纬度后csv文件.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    kinds_dict = {}
    for row in rows:
        if row[1] not in kinds_dict:
            kinds_dict[row[1]] = 1
        else:
            kinds_dict[row[1]] += 1
    # 统计数量排名前10项，剩下的用others表示,按照字典的值进行排序
    sorted_dict_dsc = sorted(kinds_dict.items(), key=lambda items: items[1], reverse=True)
    # value来统计字典的值的集合
    value = 0
    for i in range(len(sorted_dict_dsc)):
       value += int(sorted_dict_dsc[i][1])
    # keys和values用来存储前十项
    keys = []
    values = []
    new_value = 0
    for i in range(10):
        keys.append(sorted_dict_dsc[i][0])
        values.append(int(sorted_dict_dsc[i][1]) / value)
        new_value += int(sorted_dict_dsc[i][1])
    keys.append('other')
    values.append((value - new_value) / value)
    # 现在可以画图了
    fig = plt.figure()
    # 百分数保留小数点后两位
    plt.pie(values, labels=keys, autopct='%1.2f%%')
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title("站点分类饼状图")
    plt.savefig(path + '/' + '分类饼状图.png')
    plt.show()

# 6、找到带永嘉的公司，统计下种类占比,绘制一下柱状图
def paint_histogram_picture():
    f = open(path + '/' + '处理添加经纬度后csv文件.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    new_rows = []
    for row in rows:
        if '永嘉' in row[2]:
            new_rows.append(row)
        else:
            pass
    kinds_dict = {}
    for row in new_rows:
        if row[0] not in kinds_dict:
            kinds_dict[row[0]] = 1
        else:
            kinds_dict[row[0]] += 1
    # print(kinds_dict) 得出只有{'标准排放口': 50, '废气排放口': 10, '1号炉': 2, '进水口': 4, '2号炉': 2}
    keys = []
    values = []
    for key,value in kinds_dict.items():
        keys.append(key)
        values.append(value)
    plt.bar(range(len(keys)),values,color='rgb',tick_label=keys)
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title("永嘉污染分类柱状图")
    plt.savefig(path + '/' + '永嘉污染分类柱状图.png')
    plt.show()


# 7、绘制整个行业的饼图
def paint_pie_all_datas():
    f = open(path + '/' + '处理添加经纬度后csv文件.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    kinds_dict = {}
    for row in rows:
        if row[0] not in kinds_dict:
            kinds_dict[row[0]] = 1
        else:
            kinds_dict[row[0]] += 1
    # 统计数量排名前10项，剩下的用others表示,按照字典的值进行排序
    sorted_dict_dsc = sorted(kinds_dict.items(), key=lambda items: items[1], reverse=True)
    # value来统计字典的值的集合
    value = 0
    for i in range(len(sorted_dict_dsc)):
        value += int(sorted_dict_dsc[i][1])
    # keys和values用来存储前十项
    keys = []
    values = []
    new_value = 0
    for i in range(len(sorted_dict_dsc)):
        keys.append(sorted_dict_dsc[i][0])
        values.append(int(sorted_dict_dsc[i][1]) / value)
        new_value += int(sorted_dict_dsc[i][1])
    x = [int(i*100) for i in values]
    # 删除一些特别小的点，统计的其他类型中
    # 统计删除了哪些点
    """
        0 锅炉
        0 daxingchuqinyangzhi
        0 合成革
        0 啤酒
        0 工业炉窑
        0 其他（废气）
        0 ﻿皮革
    """
    keys = keys[:14]
    x = x[:14]
    keys[7] = "空格"
    keys.append("其他")
    x.append(10)
    # 现在可以画图了
    fig = plt.figure()
    # 我们将数据小的突出显示
    indic = []
    for value in x:
        if value <= x[-10]:
            indic.append(0.2)
        else:
            indic.append(0)
    # 防止标签重叠，可以将窗口设置的大一些
    plt.figure(figsize=(20, 16))
    # 百分数保留小数点后两位
    plt.pie(x, labels=keys, autopct='%1.2f%%',shadow=False,startangle=150,explode=tuple(indic))
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.savefig(path + '/' + '行业分类饼状图.png')
    plt.show()


if __name__ == '__main__':
    # 函数要按照顺序执行哦
    # change_xls_to_csv()
    # get_effective_information()
    # get_latitude_and_longitude_by_location()
    delete_useless_row()
    """上面函数执行过一次就没必要多次执行了"""
    paint_pie_picture()
    paint_histogram_picture()
    paint_pie_all_datas()
