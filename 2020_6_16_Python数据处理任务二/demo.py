"""
    任务二、中风发病因素统计分析
    要求：
        使用python的内置的数据结构完成1~3题
        读取Excel：xlrd模块
        数据可视化：matplotlib
    说明：
        数据（见Appendix-C1）来源于中国某城市各家医院2007年1月至2010年12月的脑卒中发病病例信息以及相应期间当地的逐日气象资料（Appendix-C2）。
        （数据文件夹：任务2_中风发病因素统计分析_数据）
"""
import os
import xlrd
import csv
import matplotlib.pyplot as plt
from matplotlib import font_manager


# Step1、处理数据集中的问题数据
"""
    任务提供的数据中存在哪些问题？
    请对问题数据进行标注并以附件的形式提交，拟采用csv文件
    请采取适当地修改方式处理这些问题数据
"""
# 使用so.listdir()将Appendix-C1内的excel文件以列表的形式全部显示出来
excel_file_names = os.listdir('任务2_中风发病因素分析_数据/Appendix-C1')


# 以下为按职业来统计的一些数据,1~8共8个职业
# 考虑到复杂度，决定使用函数来解决，以使代码简练




def get_messages(params):
    # 通过创建csv文件，将数据写到csv中,newline=""是不用空行，编码设置utf-8-sig这样打开就不会出现乱码
    with open("问题数据合集.csv",mode="w",newline="",encoding="utf-8-sig") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(['Sex','Age','Occupation','Time of incidence','Report time','问题数据位置'])
    f.close()

    # 第三问：创建一个列表保存所有患病者的年龄
    all_ages = []
    boys_ages_three = []
    girls_ages_three = []
    x = params
    # 下面定义的是2问的第2小问的一些临时参数
    total_b = 0
    total_b_three = []
    ages_b = 0
    boys_b = 0
    girls_b = 0
    boy_b_ages = 0
    girl_b_ages = 0
    standard_b = 0
    standard_b_boys = 0
    standard_b_girls = 0
    # 分别用来统计年龄和职业、性别、发病时间、诊断报告出错的行数
    age_error = 0
    Occupation_error = 0
    sex_error = 0
    incidence_error = 0
    rebort_error = 0
    # 统计患者的总人数以及总发病年龄
    total_persons = 0
    total_ages = 0
    # 发病年龄的标准差
    standard = 0

    # 男性的人数、年龄、标准差
    boys = 0
    boy_ages = 0
    boy_standard = 0

    # 女性的人数、年龄、标准差
    girls = 0
    girl_ages = 0
    girl_standard = 0
    # 使用for循环依次遍历列表中的每一个excel文件
    for excel_file_name in excel_file_names:
        # 发现四个excel文件只有一个sheet，且名字都是"脑卒中"，于是可以直接进行sheet操作
        excel_table = xlrd.open_workbook('任务2_中风发病因素分析_数据/Appendix-C1/%s' % excel_file_name)
        # 根据表的名称获取表的对象
        sheet = excel_table.sheet_by_name("脑卒中")
        # 根据excel文件发现，第一行都是中文列名，于是从第二行开始遍历,sheet.nrows是表的所有行数
        for i in range(1, sheet.nrows):
            """现在开始判断问题数据"""
            # 第一步是判断sheet第一列性别：性别只有1和2，如果出现其他数字或空，则为问题数据
            # sheet.row_values(i)[0]表示的是性别数据
            f = open('问题数据合集.csv', mode="a+", newline="", encoding="utf-8-sig")
            csv_write = csv.writer(f)
            try:
                if (float(sheet.row_values(i)[0]) in [1.0, 2.0]):
                    # 在性别一列没有出现问题的情况下，现在考虑表中第二列Age
                    if (sheet.row_values(i)[1] != ''):
                        if (str(sheet.row_values(i)[1]).strip() == '###'):
                            error_message = excel_file_name + '-' + "脑卒中" + '-' + str(i + 1) + "行年龄有问题！"
                            age_error += 1
                            csv_write.writerow([sheet.row_values(i)[0], sheet.row_values(i)[1], sheet.row_values(i)[2],sheet.row_values(i)[3], sheet.row_values(i)[4], error_message])
                        else:
                            # 在年龄一列没有出现问题的情况下，现在考虑第三列Occupation
                            all_ages.append(float(sheet.row_values(i)[1]))
                            if ((sheet.row_values(i)[2] != '') and (int(sheet.row_values(i)[2]) in [1, 2, 3, 4, 5, 6, 7, 8])):
                                # 此时的数据视为非问题数据
                                if(int(float(sheet.row_values(i)[0])) == 1):
                                    boys_ages_three.append(float(sheet.row_values(i)[1]))
                                else:
                                    girls_ages_three.append(float(sheet.row_values(i)[1]))
                                if(x == 1):
                                    total_b += 1
                                    ages_b += float(sheet.row_values(i)[1])
                                    standard_b += ((float(sheet.row_values(i)[1]) - 71.25587572711072) ** 2)
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    # 男性
                                    if(int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) -70.17442336563396)**2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1])-72.30629018360177)**2)
                                if(x == 2):
                                    total_b += 1
                                    ages_b += float(sheet.row_values(i)[1])
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    standard_b += ((float(sheet.row_values(i)[1]) - 761.24545829892651) ** 2)
                                    # 男性
                                    if (int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) - 61.10631443298969) ** 2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1]) - 61.49367816091954) ** 2)
                                if(x == 3):
                                    total_b += 1
                                    ages_b += float(sheet.row_values(i)[1])
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    standard_b += ((float(sheet.row_values(i)[1]) - 72.72521843928894) ** 2)
                                    # 男性
                                    if (int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) - 72.6885762794082) ** 2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1]) - 72.78528827037773) ** 2)
                                if(x == 4):
                                    total_b += 1
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    ages_b += float(sheet.row_values(i)[1])
                                    standard_b += ((float(sheet.row_values(i)[1]) - 66.96296296296296) ** 2)
                                    # 男性
                                    if (int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) - 66.50920245398773) ** 2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1]) - 68.35849056603773) ** 2)
                                if(x == 5):
                                    total_b += 1
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    ages_b += float(sheet.row_values(i)[1])
                                    standard_b += ((float(sheet.row_values(i)[1]) - 62.696969696969695) ** 2)
                                    # 男性
                                    if (int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) - 64.5813953488372) ** 2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1]) - 59.17391304347826) ** 2)
                                if(x == 6):
                                    total_b += 1
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    ages_b += float(sheet.row_values(i)[1])
                                    standard_b += ((float(sheet.row_values(i)[1]) - 63.6) ** 2)
                                    # 男性
                                    if (int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) - 63.815384615384616) ** 2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1]) - 63.04) ** 2)
                                if(x == 7):
                                    total_b += 1
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    ages_b += float(sheet.row_values(i)[1])
                                    standard_b += ((float(sheet.row_values(i)[1]) -68.699149298171) ** 2)
                                    # 男性
                                    if (int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) - 67.62362241520309) ** 2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1]) - 69.99329928307014) ** 2)
                                if(x == 8):
                                    total_b += 1
                                    total_b_three.append(float(sheet.row_values(i)[1]))
                                    ages_b += float(sheet.row_values(i)[1])
                                    standard_b += ((float(sheet.row_values(i)[1]) - 70.93858394030968) ** 2)
                                    # 男性
                                    if (int(sheet.row_values(i)[0]) == 1):
                                        boys_b += 1
                                        boy_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_boys += ((float(sheet.row_values(i)[1]) - 69.97764814051551) ** 2)
                                    else:
                                        girls_b += 1
                                        girl_b_ages += float(sheet.row_values(i)[1])
                                        standard_b_girls += ((float(sheet.row_values(i)[1]) - 72.04486842625005) ** 2)

                                # 在职位一列没有出现问题的情况下，现在考虑第四列Time of incidence
                                if (sheet.row_values(i)[3] != '' and '-' not in str(sheet.row_values(i)[3]).strip()):
                                    # 最后判断诊断时间的出错数据
                                    if (sheet.row_values(i)[3] != '' and '-' not in str(sheet.row_values(i)[3]).strip()):
                                        pass
                                    else:
                                        error_message = excel_file_name + '-' + "脑卒中" + '-' + str(i + 1) + "行诊断时间有问题！"
                                        rebort_error += 1
                                        csv_write.writerow([sheet.row_values(i)[0], sheet.row_values(i)[1], sheet.row_values(i)[2],sheet.row_values(i)[3], sheet.row_values(i)[4], error_message])
                                else:
                                    error_message = excel_file_name + '-' + "脑卒中" + '-' + str(i + 1) + "行发病时间有问题！"
                                    incidence_error += 1
                                    csv_write.writerow([sheet.row_values(i)[0], sheet.row_values(i)[1], sheet.row_values(i)[2],sheet.row_values(i)[3], sheet.row_values(i)[4], error_message])
                            else:
                                error_message = excel_file_name + '-' + "脑卒中" + '-' + str(i + 1) + "行职业有问题！"
                                Occupation_error += 1
                                csv_write.writerow([sheet.row_values(i)[0], sheet.row_values(i)[1], sheet.row_values(i)[2],sheet.row_values(i)[3], sheet.row_values(i)[4], error_message])
                                # 问题数据的处理部分，超过55岁且职位是空的记为8，否则是7
                                if (float(sheet.row_values(i)[1]) > 55):
                                    Occupation = 8
                                    if (x == Occupation):
                                        total_b += 1
                                        ages_b += float(sheet.row_values(i)[1])
                                        total_b_three.append(float(sheet.row_values(i)[1]))
                                        standard_b += ((float(sheet.row_values(i)[1]) - 70.93858394030968) ** 2)
                                        # 男性
                                        if (int(sheet.row_values(i)[0]) == 1):
                                            boys_b += 1
                                            boy_b_ages += float(sheet.row_values(i)[1])
                                            standard_b_boys += ((float(sheet.row_values(i)[1]) - 69.97764814051551) ** 2)
                                        else:
                                            girls_b += 1
                                            girl_b_ages += float(sheet.row_values(i)[1])
                                            standard_b_girls+= ((float(sheet.row_values(i)[1]) - 72.04486842625005) ** 2)
                                else:
                                    Occupation = 7
                                    if (x == Occupation):
                                        total_b += 1
                                        ages_b += float(sheet.row_values(i)[1])
                                        total_b_three.append(float(sheet.row_values(i)[1]))
                                        standard_b += ((float(sheet.row_values(i)[1]) - 68.699149298171) ** 2)
                                        # 男性
                                        if (int(sheet.row_values(i)[0]) == 1):
                                            boys_b += 1
                                            boy_b_ages += float(sheet.row_values(i)[1])
                                            standard_b_boys += ((float(sheet.row_values(i)[1]) - 67.62362241520309) ** 2)
                                        else:
                                            girls_b += 1
                                            girl_b_ages += float(sheet.row_values(i)[1])
                                            standard_b_girls += ((float(sheet.row_values(i)[1]) - 69.99329928307014) ** 2)

                            # 后面的时间等有空的数据虽是问题数据，但是不影响正常的使用
                            total_ages += float(sheet.row_values(i)[1])
                            total_persons += 1
                            standard += ((float(sheet.row_values(i)[1]) - 69.71744364261313) ** 2)
                            if (float(sheet.row_values(i)[0]) == 1.0):
                                boy_ages += float(sheet.row_values(i)[1])
                                boys += 1
                                boy_standard += ((float(sheet.row_values(i)[1]) - 68.62856201120667) ** 2)
                            else:
                                girl_ages += float(sheet.row_values(i)[1])
                                girls += 1
                                girl_standard += ((float(sheet.row_values(i)[1]) - 70.99232599894655) ** 2)
                    else:
                        # 显示哪些Age为空的单元格
                        error_message = excel_file_name + '-' + "脑卒中" + '-' + str(i + 1) + "行年龄有问题！"
                        age_error += 1
                        csv_write.writerow([sheet.row_values(i)[0], sheet.row_values(i)[1], sheet.row_values(i)[2],sheet.row_values(i)[3], sheet.row_values(i)[4], error_message])
                else:
                    error_message = excel_file_name + '-' + "脑卒中" + '-' + str(i + 1) + "行性别有问题！"
                    sex_error += 1
                    csv_write.writerow([sheet.row_values(i)[0], sheet.row_values(i)[1], sheet.row_values(i)[2], sheet.row_values(i)[3],sheet.row_values(i)[4], error_message])

            except Exception as error:
                error_message = excel_file_name + '-' + "脑卒中" + '-' + str(i + 1) + "行性别有问题！"
                sex_error += 1
                csv_write.writerow([sheet.row_values(i)[0], sheet.row_values(i)[1], sheet.row_values(i)[2], sheet.row_values(i)[3],sheet.row_values(i)[4], error_message])
            """
                data2.xls的2635/5603/5980/6238/7829/7994/8845/10236/13963/14854/15696/17979性别是空的，记为问题数据
            """
    if (x == 0):
        print("Appendix-C1的excel文件中年龄和性别出错、职位出错、发病时间、诊断时间出错的数目分别是:{},{},{},{},{}".format(age_error, sex_error,Occupation_error, incidence_error,rebort_error))
        # 这边因为if循环多层嵌套，所以有些事前面数据错了，后面数据也错了，这样后面数据报错数就没计算

        # Step2、统计以下指标
        """
            1）患者的总人次、发病年龄的平均值和标准差，再按性别分开来统计男性和女性患者的人数、比例、年龄均值、年龄标准差
            2）按职业统计：患者的总人次以及发病年龄的平均值和标准差，再按性别分开来统计男性和女性患者的人数、比例、年龄均值、年龄标准差
        """
        average_ages = total_ages / total_persons
        # 为了计算方便，将得到的发病年龄的平均值得到的结果带到了if里面做标准差，否则又要复制不少代码
        print("患者的总人次、发病年龄的平均值及标准差是：{},{},{}".format(total_persons, average_ages, standard / total_persons))
        # 同样将得到的男性和女性年龄的平均值用到前面，理由也是要么代码要复制一大堆
        print("男性患者的人数、比例、年龄均值、年龄标准差分别是：{},{},{},{}".format(boys, boys / total_persons, boy_ages / boys, boy_standard / boys))
        print("女性患者的人数、比例、年龄均值、年龄标准差分别是：{},{},{},{}".format(girls, girls / total_persons, girl_ages / girls,girl_standard / girls))
    elif(x in [1,2,3,4,5,6,7,8]):
        return(total_b,ages_b/total_b,standard_b/total_b,boys_b,boy_b_ages/boys_b,standard_b_boys/boys_b,girls_b,girl_b_ages/girls_b,standard_b_girls/girls_b,total_b_three)
    else:
        return(all_ages,boys_ages_three,girls_ages_three)
# 这边显示的是1问及2问的第一部分
get_messages(0)

# 以下是第二题的2问，分别是1~8所代表的职业的数据
# print(get_messages(1))
# print(get_messages(2))
# print(get_messages(3))
# print(get_messages(4))
# print(get_messages(5))
# print(get_messages(6))
# print(get_messages(7))
# print(get_messages(8))

# Step3、如何对下列数据进行可视化
"""
    a)做出所有发病患者的年龄分布图
    b)按性别：做出发病患者的年龄分布图
    c）按职业：做出年龄分布图
    d）统计每天、每月的患者人数，并将该数据进行可视化
"""
# 先创建一目录，用于保存可视化的图片
path ='可视化图片'
# 没有此目录则创建此目录
if not os.path.exists(path):
    os.mkdir(path)

# a、做出所有发病患者的年龄分布图
all_ages,boys_ages_three,girls_ages_three = get_messages(9)
# 因为人数过多，这边打算分区间显示0~30/30~50/50~60/60~70/70~100
age_0_30 = 0
age_30_50 = 0
age_50_60 = 0
age_60_70 = 0
age_70_100 = 0

for age in all_ages:
    if (age > 0  and age <= 30):
        age_0_30 += 1
    elif(age > 30 and age <= 50):
        age_30_50 += 1
    elif(age > 50 and age <= 60):
        age_50_60 += 1
    elif(age > 60 and age <= 70):
        age_60_70 += 1
    else:
        age_70_100 += 1
ages_now = [age_0_30,age_30_50,age_50_60,age_60_70,age_70_100]
x1 = ['0~30','30~50','50~60','60~70','70~100']
plt.bar(x1,ages_now, align='center',label="所有发病患者年龄分布图")
plt.xlabel('年龄区间')
plt.ylabel('人数')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('所有发病患者的年龄分布图')
plt.legend()
plt.savefig(path + '/' + 'all_ages.png')
plt.show()







# 按性别：做出发病患者的年龄分布图
# 因为人数过多，这边打算分区间显示0~30/30~50/50~60/60~70/70~100
age_0_30_boys = 0
age_30_50_boys = 0
age_50_60_boys = 0
age_60_70_boys = 0
age_70_100_boys = 0

for age in boys_ages_three:
    if (age > 0  and age <= 30):
        age_0_30_boys += 1
    elif(age > 30 and age <= 50):
        age_30_50_boys += 1
    elif(age > 50 and age <= 60):
        age_50_60_boys += 1
    elif(age > 60 and age <= 70):
        age_60_70_boys += 1
    else:
        age_70_100_boys += 1
ages_now_boys = [age_0_30_boys,age_30_50_boys,age_50_60_boys,age_60_70_boys,age_70_100_boys]
x1 = ['0~30','30~50','50~60','60~70','70~100']
plt.bar(x1,ages_now_boys, align='center',label="男性年龄分布图")
plt.xlabel('人数')
plt.ylabel('年龄区间')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('男性发病患者的年龄分布图')
plt.legend()
plt.savefig(path + '/' + 'boys_ages.png')
plt.show()

age_0_30_girls = 0
age_30_50_girls = 0
age_50_60_girls = 0
age_60_70_girls = 0
age_70_100_girls = 0

for age in girls_ages_three:
    if (age > 0  and age <= 30):
        age_0_30_girls += 1
    elif(age > 30 and age <= 50):
        age_30_50_girls += 1
    elif(age > 50 and age <= 60):
        age_50_60_girls += 1
    elif(age > 60 and age <= 70):
        age_60_70_girls += 1
    else:
        age_70_100_girls += 1
ages_now_girls = [age_0_30_girls,age_30_50_girls,age_50_60_girls,age_60_70_girls,age_70_100_girls]
x1 = ['0~30','30~50','50~60','60~70','70~100']
plt.bar(x1,ages_now_girls, align='center',label="女性年龄分布图")
plt.xlabel('人数')
plt.ylabel('年龄区间')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title('女性发病患者的年龄分布图')
plt.legend()
plt.savefig(path + '/' + 'girls_ages.png')
plt.show()

# 按职业：做出年龄分布图
for i in range(1,9):
    t1, a1, s1, b1, b2, s2, g1, g2, s3, total_b_three = get_messages(i)
    positions = ['农民','工人','退休人员','教师','渔民','医务人员','职工','离退人员']
    print("{}所以发病患者人数是{},其中年龄的均值是:{},年龄的标准差是：{},其中男性患者的人数是:{},年龄均值是{},年龄标准差是：{},女性患者人数是：{},年龄均值是：{},年龄标准差是：{}".format(positions[i-1],t1, a1, s1, b1, b2, s2, g1, g2, s3))
    print("男性比例是：{}，女性比例是：{}".format(b1/t1,g1/t1))
    age_0_30 = 0
    age_30_50 = 0
    age_50_60 = 0
    age_60_70 = 0
    age_70_100 = 0

    for age in total_b_three:
        age = float(age)
        if (age > 0 and age <= 30):
            age_0_30 += 1
        elif (age > 30 and age <= 50):
            age_30_50 += 1
        elif (age > 50 and age <= 60):
            age_50_60 += 1
        elif (age > 60 and age <= 70):
            age_60_70 += 1
        else:
            age_70_100 += 1
    ages_now = [age_0_30, age_30_50, age_50_60, age_60_70, age_70_100]
    x1 = ['0~30', '30~50', '50~60', '60~70', '70~100']
    plt.bar(x1, ages_now, align='center',label="职业年龄分布图")
    plt.xlabel('人数')
    plt.ylabel('年龄区间')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.title('{}患者的年龄分布图'.format(positions[i-1]))
    plt.legend()
    plt.savefig(path + '/' + '{}_ages.png'.format(positions[i-1]))
    plt.show()

# 统计每天、每月的患者人数，并将该数据进行可视化
