#coding:utf-8
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

"""
    先把附件1的[进项发票信息]按照[有效发票/无效发票]分成两个csv文件
"""
path = 'Task1'
if not os.path.exists(path):
    os.mkdir(path)
path_now = path + '/' + 'pictures'
if not os.path.exists(path_now):
    os.mkdir(path_now)


def divide_csv():
    # 企业代号	发票号码	 开票日期	销方单位代号	 金额	 税额	 价税合计	 发票状态
    # ['E70', '5241999', '2018/5/16', 'A06470', '106.44', '17.03', '123.47', '有效发票']
    effective_file = open(path + '/' + '1_进项有效发票信息.csv', mode='w', encoding='utf-8-sig', newline='')
    effective_write = csv.writer(effective_file)
    effective_write.writerow(['企业代号', '发票号码', '开票日期', '销方单位代号', '金额', '税额', '价税合计', '发票状态'])

    void_file = open(path + '/' + '2_进项作废发票信息.csv', mode='w', encoding='utf-8-sig', newline='')
    void_write = csv.writer(void_file)
    void_write.writerow(['企业代号', '发票号码', '开票日期', '销方单位代号', '金额', '税额', '价税合计', '发票状态'])
    with open('1_2_进项发票信息.CSV', mode='r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if '有效发票' in row:
                effective_write.writerow(row)
            elif '作废发票' in row:
                void_write.writerow(row)
    f.close()
    effective_file.close()
    void_file.close()



"""
    下面来对有效发票信息进行处理，保存相应的数据
"""
def deal_with_effective_file():
    fp = open('Task1/1_进项有效发票信息.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(fp)
    # 使用for循环生成[企业代号]的列表
    bussiness_numbers = []
    for i in range(1,124):
        bussiness_numbers.append('E'+str(i))
    # 创建空列表准备存放对应的交易信息
    lists = [[] for i in range(1,124)]
    # 创建空列表存放交易月份信息
    dates = [[] for i in range(1,124)]
    months = []
    for row in csv_reader:
        for i in range(len(bussiness_numbers)):
            if row[0] == bussiness_numbers[i]:
                lists[i].append(row)
                dates[i].append(row[2])
    for date in dates:
        first_year = int(str(date[-1]).split('/')[0])
        first_month = int(str(date[-1]).split('/')[1])
        second_year = int(str(date[0]).split('/')[0])
        second_month = int(str(date[0]).split('/')[1])
        months.append(12*(first_year-second_year) + (first_month-second_month))
    # 下面开始统计合作单位的代号以及成交额
    # 再次创建空列表存储价税合计的值
    values = []
    # 创建空字典存放负数发票数以及负数发票数占比
    negative_numbers = []
    total_numbers = []
    for num in lists:
        # 每个代号所代表的公司初始交易额都是0
        value = 0
        negative_number = 0
        total_number = 0
        for i in num:
            value += float(i[6])
            total_number += 1
            if (float(i[4]) < 0):
                negative_number += 1
        values.append(value)
        negative_numbers.append(negative_number)
        if total_number != 0:
            total_numbers.append(negative_number/total_number * 100)
        else:
            total_numbers.append(0)
    # 现在统计合作单位分别是哪些
    bussiness_friends = [[] for i in range(1,124)]
    for i in range(len(bussiness_friends)):
        for friend in lists[i]:
            if friend[3] not in bussiness_friends[i]:
                bussiness_friends[i].append(friend[3])
    # 现在统计每个代号所代表的单位的合作单位的个数
    bussiness_friends_numbers = []
    for friend in bussiness_friends:
        bussiness_friends_numbers.append(len(friend))
    # 现在计算每月平均金额
    average_value = []
    for j in range(len(values)):
        if months[j] != 0:
            average_value.append(values[j]/months[j])
        else:
            average_value.append(values[j])
    return(values,bussiness_friends,bussiness_friends_numbers,bussiness_numbers,lists,months,average_value,negative_numbers,total_numbers)

def deal_with_invalid_file():
    fp = open('Task1/2_进项作废发票信息.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(fp)
    # 使用for循环生成[企业代号]的列表
    bussiness_numbers = []
    for i in range(1, 124):
        bussiness_numbers.append('E' + str(i))
    # 创建空列表准备存放对应的交易信息
    lists = [[] for i in range(1, 124)]
    for row in csv_reader:
        for i in range(len(bussiness_numbers)):
            if row[0] == bussiness_numbers[i]:
                lists[i].append(row)
    # 下面开始统计合作单位的代号以及成交额
    # 再次创建空列表存储价税合计的值
    values = []
    for num in lists:
        # 每个代号所代表的公司初始交易额都是0
        value = 0
        for i in num:
            value += float(i[6])
        values.append(value)
    # 现在统计合作单位分别是哪些
    bussiness_friends = [[] for i in range(1, 124)]
    for i in range(len(bussiness_friends)):
        for friend in lists[i]:
            if friend[3] not in bussiness_friends[i]:
                bussiness_friends[i].append(friend[3])
    # 现在统计每个代号所代表的单位的合作单位的个数
    bussiness_friends_numbers = []
    for friend in bussiness_friends:
        bussiness_friends_numbers.append(len(friend))
    return (values, bussiness_friends, bussiness_friends_numbers, bussiness_numbers, lists)

# 由于此函数执行时间久，打算第一次生成文件后便不再使用
def save_values_with_every_bussiness():
    values, bussiness_friends, bussiness_friends_numbers, bussiness_numbers,lists,months,average_value,negative_numbers,total_numbers = deal_with_effective_file()
    # 现在来分别统计每个单位所代表的合作单位的成交额是多少
    values_with_friends = [[] for i in range(1,124)]
    i = 0
    for friend in bussiness_friends:
        # 合作单位列表中的每个具体的单位编号
        for m in friend:
            # 设置一个变量，存放每个编号的金额
            money = 0
            # 存放的是所有信息的列表
            for j in lists[i]:
                # 判断合作单位的编号是否和列表中第3个位置的信息一致，是的话就把金额相加
                if j[3] == m:
                    money += float(j[6])
            values_with_friends[i].append(money)
        i += 1
    f = open(path + '/' + '3_每个编号所对应的合作单位交易额.csv',mode='w',encoding='utf-8-sig',newline='')
    csv_write = csv.writer(f)
    for i in range(len(bussiness_friends)):
        csv_write.writerow(bussiness_friends[i])
        csv_write.writerow(values_with_friends[i])
    f.close()

"""
    现在开始处理附加1的[销项发票信息],和前面的步骤基本是一致的
"""
def divide_sale_csv():
    # 企业代号	发票号码	 开票日期	销方单位代号	 金额	 税额	 价税合计	 发票状态
    # ['E70', '5241999', '2018/5/16', 'A06470', '106.44', '17.03', '123.47', '有效发票']
    effective_file = open(path + '/' + '4_销项有效发票信息.csv', mode='w', encoding='utf-8-sig', newline='')
    effective_write = csv.writer(effective_file)
    effective_write.writerow(['企业代号', '发票号码', '开票日期', '销方单位代号', '金额', '税额', '价税合计', '发票状态'])

    void_file = open(path + '/' + '5_销项作废发票信息.csv', mode='w', encoding='utf-8-sig', newline='')
    void_write = csv.writer(void_file)
    void_write.writerow(['企业代号', '发票号码', '开票日期', '销方单位代号', '金额', '税额', '价税合计', '发票状态'])
    with open('销项发票信息.csv', mode='r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if '有效发票' in row:
                effective_write.writerow(row)
            elif '作废发票' in row:
                void_write.writerow(row)
    f.close()
    effective_file.close()
    void_file.close()

def deal_with_effective_sale_file():
    fp = open('Task1/4_销项有效发票信息.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(fp)
    # 使用for循环生成[企业代号]的列表
    bussiness_numbers = []
    for i in range(1,124):
        bussiness_numbers.append('E'+str(i))
    # 创建空列表准备存放对应的交易信息
    lists = [[] for i in range(1,124)]
    # 创建空列表存放交易月份信息
    dates = [[] for i in range(1, 124)]
    months = []
    for row in csv_reader:
        for i in range(len(bussiness_numbers)):
            if row[0] == bussiness_numbers[i]:
                lists[i].append(row)
                dates[i].append(row[2])
    for date in dates:
        first_year = int(str(date[-1]).split('/')[0])
        first_month = int(str(date[-1]).split('/')[1])
        second_year = int(str(date[0]).split('/')[0])
        second_month = int(str(date[0]).split('/')[1])
        months.append(12*(first_year-second_year) + (first_month-second_month))
    # 下面开始统计合作单位的代号以及成交额
    # 再次创建空列表存储价税合计的值
    values = []
    # 创建空字典存放负数发票数以及负数发票数占比
    negative_numbers = []
    total_numbers = []
    for num in lists:
        # 每个代号所代表的公司初始交易额都是0
        value = 0
        negative_number = 0
        total_number = 0
        for i in num:
            value += float(i[4])
            total_number += 1
            if (float(i[4]) < 0):
                negative_number += 1
        values.append(value)
        negative_numbers.append(negative_number)
        if total_number != 0:
            total_numbers.append(negative_number / total_number * 100)
        else:
            total_numbers.append(0)
    # 现在统计合作单位分别是哪些
    bussiness_friends = [[] for i in range(1,124)]
    for i in range(len(bussiness_friends)):
        for friend in lists[i]:
            if friend[3] not in bussiness_friends[i]:
                bussiness_friends[i].append(friend[3])
    # 现在统计每个代号所代表的单位的合作单位的个数
    bussiness_friends_numbers = []
    for friend in bussiness_friends:
        bussiness_friends_numbers.append(len(friend))
    # 现在计算每月平均金额
    average_value = []
    for j in range(len(values)):
        if months[j] != 0:
            average_value.append(values[j] / months[j])
        else:
            average_value.append(values[j])
    return(values,bussiness_friends,bussiness_friends_numbers,bussiness_numbers,lists,months,average_value,negative_numbers,total_numbers)

def deal_with_invalid_sale_file():
    fp = open('Task1/5_销项作废发票信息.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(fp)
    # 使用for循环生成[企业代号]的列表
    bussiness_numbers = []
    for i in range(1, 124):
        bussiness_numbers.append('E' + str(i))
    # 创建空列表准备存放对应的交易信息
    lists = [[] for i in range(1, 124)]
    for row in csv_reader:
        for i in range(len(bussiness_numbers)):
            if row[0] == bussiness_numbers[i]:
                lists[i].append(row)
    # 下面开始统计合作单位的代号以及成交额
    # 再次创建空列表存储价税合计的值
    values = []
    for num in lists:
        # 每个代号所代表的公司初始交易额都是0
        value = 0
        for i in num:
            value += float(i[6])
        values.append(value)
    # 现在统计合作单位分别是哪些
    bussiness_friends = [[] for i in range(1, 124)]
    for i in range(len(bussiness_friends)):
        for friend in lists[i]:
            if friend[3] not in bussiness_friends[i]:
                bussiness_friends[i].append(friend[3])
    # 现在统计每个代号所代表的单位的合作单位的个数
    bussiness_friends_numbers = []
    for friend in bussiness_friends:
        bussiness_friends_numbers.append(len(friend))
    return (values, bussiness_friends, bussiness_friends_numbers, bussiness_numbers, lists)

def save_values_with_sale_every_bussiness():
    values, bussiness_friends, bussiness_friends_numbers, bussiness_numbers,lists,months,average_value,negative_numbers,total_numbers = deal_with_effective_sale_file()
    # 现在来分别统计每个单位所代表的合作单位的成交额是多少
    values_with_friends = [[] for i in range(1,124)]
    i = 0
    for friend in bussiness_friends:
        # 合作单位列表中的每个具体的单位编号
        for m in friend:
            # 设置一个变量，存放每个编号的金额
            money = 0
            # 存放的是所有信息的列表
            for j in lists[i]:
                # 判断合作单位的编号是否和列表中第3个位置的信息一致，是的话就把金额相加
                if j[3] == m:
                    money += float(j[6])
            values_with_friends[i].append(money)
        i += 1
    f = open(path + '/' + '6_每个编号销项所对应的合作单位交易额.csv',mode='w',encoding='utf-8-sig',newline='')
    csv_write = csv.writer(f)
    for i in range(len(bussiness_friends)):
        csv_write.writerow(bussiness_friends[i])
        csv_write.writerow(values_with_friends[i])
    f.close()

def analyse_bussiness_information():
    values, bussiness_friends, bussiness_friends_numbers, bussiness_numbers, lists,months,average_value,negative_numbers,total_numbers= deal_with_effective_file()
    values1,bussiness_friends1,bussiness_friends_numbers1,bussiness_numbers1,lis11 = deal_with_invalid_file()

    values_sale, bussiness_friends_sale, bussiness_friends_numbers_sale, bussiness_numbers_sale, lists_sale,months_sale,average_value_sale,negative_numbers_sale,total_numbers_sale = deal_with_effective_sale_file()
    values2, bussiness_friends2, bussiness_friends_numbers2, bussiness_numbers2, lis12 = deal_with_invalid_file()

    f = open('企业信息.csv',mode='r')
    csv_reader = csv.reader(f)
    rows = []
    for row in csv_reader:
        rows.append(row)
    f.close()
    # 处理进项有效交易数据
    file = open('Task1/3_每个编号所对应的合作单位交易额.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(file)
    rows_now = []
    for row in csv_reader:
        rows_now.append(row)
    # 下面是构建列表来存储进项有效合作单位数
    effective_numbers = []
    for i in range(1,len(rows_now),2):
        num = 0
        for number in rows_now[i]:
            if number != '0.0':
                num += 1
        effective_numbers.append(num)
    file.close()

    # 下面是销项有效交易数据
    file1 = open('Task1/6_每个编号销项所对应的合作单位交易额.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(file1)
    rows_now1 = []
    for row in csv_reader:
        rows_now1.append(row)
    # 下面是构建列表来存储进项有效合作单位数
    sale_effective_numbers = []
    for i in range(1, len(rows_now1), 2):
        num = 0
        for number in rows_now1[i]:
            if number != '0.0':
                num += 1
        sale_effective_numbers.append(num)
    file1.close()

    fp = open('Task1/7_处理后企业信息.csv',mode='w',encoding='utf-8-sig',newline='')
    csv_write = csv.writer(fp)
    csv_write.writerow(['企业代号','企业名称','信誉评级','是否违约','进项价税合计','合作单位总数','有效合作单位数','作废价税合计','作废合作单位总数','进项作废/有效比%','有效/作废合作单位数比%','净利润','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项金额','销项合作单位总数','销项有效合作单位数','销项作废价税合计','销项作废合作单位总数','销项作废/有效比%','销项有效/作废合作单位数比%','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比'])
    for i in range(1,len(rows)):
        rows[i].append(values[i-1])
        rows[i].append(bussiness_friends_numbers[i-1])
        rows[i].append(effective_numbers[i-1])
        rows[i].append(values1[i-1])
        rows[i].append(bussiness_friends_numbers1[i-1])
        rows[i].append(values1[i-1]/values[i-1] * 100)
        rows[i].append(bussiness_friends_numbers1[i-1]/bussiness_friends_numbers[i-1] * 100)
        rows[i].append(values_sale[i-1] - values[i-1])
        rows[i].append(months[i-1])
        rows[i].append(average_value[i-1])
        rows[i].append(negative_numbers[i-1])
        rows[i].append(total_numbers[i-1])


        rows[i].append(values_sale[i - 1])
        rows[i].append(bussiness_friends_numbers_sale[i - 1])
        rows[i].append(sale_effective_numbers[i - 1])
        rows[i].append(values2[i - 1])
        rows[i].append(bussiness_friends_numbers2[i - 1])
        rows[i].append(values2[i - 1] / values_sale[i - 1] * 100)
        rows[i].append(bussiness_friends_numbers2[i - 1] / bussiness_friends_numbers_sale[i - 1] * 100)
        rows[i].append(months_sale[i-1])
        rows[i].append(average_value_sale[i-1])
        rows[i].append(negative_numbers_sale[i-1])
        rows[i].append(total_numbers_sale[i-1])
    for j in range(1,len(rows)):
        csv_write.writerow(rows[j])
    fp.close()


"""
    下面开始进行数据可视化
        1)进项有效合作单位数和销项有效合作单位数（分A/B/C/D都画）柱状图
        2)进项作废/有效比  和   销项作废/有效比（分A/B/C/D都画）
        3)净利润散点图（也分A/B/C/D）
"""
def prepare_painting_information():
    f = open('Task1/7_处理后企业信息.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = []
    for row in csv_reader:
        rows.append(row)
    # 对评分等级分别是A/B/C/D各自新建两个空列表，分别存放的是[进项有效合作单位数/销项有效合作单位数]
    in_bussiness_friends = [[] for i in range(4)]
    sale_bussiness_friends = [[] for i in range(4)]

    # 对评分等级分别是A/B/C/D各自新建两个空列表，分别存放的是[进项作废/有效比  销项作废/有效比]
    in_compare_bussiness = [[] for i in range(4)]
    sale_compare_bussiness = [[] for i in range(4)]

    # 下面的列表专门存放的是净利润数据
    reward = [[] for i in range(4)]

    # 下面开始遍历rows，存放到对应的列表中去
    for row in rows:
        if 'A' in row:
            in_bussiness_friends[0].append(int(row[6]))
            sale_bussiness_friends[0].append(int(row[14]))
            in_compare_bussiness[0].append(float(row[9]))
            sale_compare_bussiness[0].append(float(row[17]))
            reward[0].append(float(row[11]))
        elif 'B' in row:
            in_bussiness_friends[1].append(int(row[6]))
            sale_bussiness_friends[1].append(int(row[14]))
            in_compare_bussiness[1].append(float(row[9]))
            sale_compare_bussiness[1].append(float(row[17]))
            reward[1].append(float(row[11]))
        elif 'C' in row:
            in_bussiness_friends[2].append(int(row[6]))
            sale_bussiness_friends[2].append(int(row[14]))
            in_compare_bussiness[2].append(float(row[9]))
            sale_compare_bussiness[2].append(float(row[17]))
            reward[2].append(float(row[11]))
        elif 'D' in row:
            in_bussiness_friends[3].append(int(row[6]))
            sale_bussiness_friends[3].append(int(row[14]))
            in_compare_bussiness[3].append(float(row[9]))
            sale_compare_bussiness[3].append(float(row[17]))
            reward[3].append(float(row[11]))
        else:
            pass
    return(in_bussiness_friends,sale_bussiness_friends,in_compare_bussiness,sale_compare_bussiness,reward)

def paint_data_using_bar():
    in_bussiness_friends, sale_bussiness_friends, in_compare_bussiness, sale_compare_bussiness, reward = prepare_painting_information()
    bar_width = 0.3
    labels = ['A_进项有效合作单位数','B_进项有效合作单位数','C_进项有效合作单位数','D_进项有效合作单位数']
    labels1 = ['A_销项有效合作单位数','B_销项有效合作单位数','C_销项有效合作单位数','D_销项有效合作单位数']
    for i in range(len(in_bussiness_friends)):
        plt.bar(x=range(len(in_bussiness_friends[i])),height=in_bussiness_friends[i],label=labels[i],color='steelblue',alpha=0.8,width=bar_width)
        # 将x轴数据加上bar_width就能使得第二个柱状图和第一个并列
        plt.bar(x=np.arange(len(in_bussiness_friends[i]))+bar_width,height=sale_bussiness_friends[i],label=labels1[i],color='indianred',alpha=0.8,width=bar_width)
        # 显示中文名称
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 设置标题
        plt.title('进项有效合作单位数和销项有效合作单位数')
        # 为两条坐标轴设置名称
        plt.xlabel('序号')
        plt.ylabel('个')
        plt.legend()
        plt.savefig(path_now + '/' + '{}.png'.format(labels[i]),dpi=200)
        plt.show()
    str_now = '进项作废_有效比'
    str1_now = '销项作废_有效比'
    alphas = ['A','B','C','D']
    for i in range(len(in_compare_bussiness)):
        plt.bar(x=range(len(in_compare_bussiness[i])),height=in_compare_bussiness[i],label=alphas[i] + str_now,color='steelblue',alpha=0.8,width=bar_width)
        # 将x轴数据加上bar_width就能使得第二个柱状图和第一个并列
        plt.bar(x=np.arange(len(in_compare_bussiness[i]))+bar_width,height=sale_compare_bussiness[i],label=alphas[i] + str1_now,color='indianred',alpha=0.8,width=bar_width)
        # 显示中文名称
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 设置标题
        plt.title('进项和销项有效/作废比')
        # 为两条坐标轴设置名称
        plt.xlabel('序号')
        plt.ylabel('比值')
        plt.legend()
        plt.savefig(path_now + '/' + '{}.png'.format(alphas[i]+str_now),dpi=200)
        plt.show()
    str_h = '净利润'
    for i in range(len(reward)):
        plt.scatter(x=range(len(reward[i])),y=reward[i],s=20)
        # 显示中文名称
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 设置标题
        plt.title('净利润')
        # 为两条坐标轴设置名称
        plt.xlabel('序号')
        plt.ylabel('元')
        plt.savefig(path_now + '/' + '{}.png'.format(alphas[i]+str_h),dpi=200)
        plt.show()



if __name__ == '__main__':
    divide_csv()
    divide_sale_csv()
    deal_with_invalid_sale_file()
    save_values_with_sale_every_bussiness()
    deal_with_effective_file()
    deal_with_invalid_file()
    analyse_bussiness_information()
    deal_with_effective_sale_file()
    save_values_with_every_bussiness()
    prepare_painting_information()
    paint_data_using_bar()