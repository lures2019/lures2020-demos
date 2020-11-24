"""
    解题的思路大致如下：
        1）先根据产品id：逐一得到对应的产品2014年末的存货量和成本价
        2）再根据买入量和卖出量，确定Cij甚至是Cij+1
        3）依次计算得到每行数据的盈利
        4）统计前3个月各个盈利商的交易类型2的盈利情况
        5）总计算整个市场的交易类型2的盈利情况
"""
import xlrd

# 使用xlrd模块加载要处理的Excel文件
wb = xlrd.open_workbook('盈利计算.xlsx')
# 通过使用wb.sheet_names()显示当前的Excel文件的所有数据表
use_sheet = wb.sheet_by_name(wb.sheet_names()[1])
compare_sheet = wb.sheet_by_name(wb.sheet_names()[0])
# 按行读取use_sheet数据表的数据
use_row = []
for row in range(use_sheet.nrows):
    use_row.append(use_sheet.row_values(row))
# 同理按行加载compare_sheet数据表的数据
compare_row = []
for row in range(compare_sheet.nrows):
    compare_row.append(compare_sheet.row_values(row))
# 先统计交易商businessman的人数
businessman = []
for i in range(1,len(use_row)):
    # 先判断列表中有没有当前的交易商，有的话pass，没的话加进列表中
    if use_row[i][2] not in businessman:
        businessman.append(use_row[i][2])
    else:
        pass
print("当前{}数据表中共有{}名交易商，分别是{}".format(wb.sheet_names()[1],len(businessman),businessman))
# 创建交易商列表来存储每个交易商3个月内的类型2的盈利
income = []
for man in businessman:
    # 用来存储每个交易商的前3月份收入情况
    sum = 0
    # 存储产品的id，用来判断此前有没有购买过此款产品
    ids = []
    # 存储之前出现过产品的成本
    my_dict = {}
    for i in range(1,len(use_row)):
        # 判断use_row中每行的交易商是否和第一层for循环中的一致
        if(use_row[i][2] == man):
            """查看当天对应的类型2产品的卖出量以及卖价，找到另一个sheet中的成本价"""
            """相同的交易商可能时隔多日选择相同的产品进行购买或卖出，此时如果是产品1，会影响之后的成本价格"""
            # 现在寻找相同的产品id,如果用别的数据类型的话可能会超出范围
            id = str(use_row[i][1])
            # 代表此前没有出现过的产品id
            if (id not in ids):
                for j in range(1,len(compare_row)):
                    # 在另一张sheet中，如果交易商以及产品id都相同，记录初始的成本以及存货
                    if (compare_row[j][2] == man and str(compare_row[j][1]) == id):
                        # u记录库存量，p0代表成本价
                        u = float(compare_row[j][3])
                        p0 = float(compare_row[j][4])
                        # 计算买入量和卖出量之差
                        if use_row[i][5] == '':
                            Q = use_row[i][4]
                        else:
                            Q = use_row[i][4] - use_row[i][5]
                        # 计算成本
                        C = (u * p0 + Q * float(use_row[i][3])) / (u + Q)
                        if (use_row[i][6] == 2.0):
                            sum += (Q * float(use_row[i][3]) - Q * C)
                            if(str(id) not in my_dict):
                                my_dict[str(id)] = C + Q
                        else:
                            if(str(id) not in my_dict):
                                my_dict[str(id)] = C + Q
                        break
            else:
                for j in range(1,len(compare_row)):
                    # 在另一张sheet中，如果交易商以及产品id都相同，记录初始的成本以及存货
                    if (compare_row[j][2] == man and str(compare_row[j][1]) == id):
                        # u记录库存量，p0代表成本价
                        u = float(compare_row[j][3])
                        p0 = float(compare_row[j][4])
                        # 计算买入量和卖出量之差
                        if use_row[i][5] == '':
                            Q = use_row[i][4]
                        else:
                            Q = use_row[i][4] - use_row[i][5]
                        if (use_row[i][6] == 2.0):
                            # 计算成本
                            C = my_dict[str(id)] + Q
                            sum += (Q * float(use_row[i][3]) - Q * C)
                        else:
                            C = my_dict[str(id)] + Q
                            my_dict[str(id)] = C
                        break
            # 将产品id添加到列表中
            ids.append(id)
    income.append(sum)
print('{}名交易商前3个月的类型2的盈利情况是：{}'.format(len(businessman),income))
mall = 0
for x in income:
    mall += x
print('市场类型2的盈利情况是{}'.format(mall))