import os
import matplotlib.pyplot as plt
import csv



def draw_city_histogram():
    # 读取爬取的招聘信息表，统计不同城市提供的岗位数量
    f = open('财汇专业招聘岗位信息表.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 创建城市字典
    city_dict = {}
    # 第一行是标头，可以直接跳过
    for row in rows[1:]:
        # 如果字典中有这个城市，则城市的值+1，否则直接赋值为1
        if row[4] not in city_dict:
            city_dict[row[4]] = 1
        else:
            city_dict[row[4]] += 1
    # 将岗位数量为1的城市都归结为    其他城市
    # 创建新字典new_dict
    new_dict = {}
    count = 0
    for key,value in city_dict.items():
        if value == 1 or value == 2:
            count += value
        else:
            new_dict[key] = value
    new_dict["其他城市"] = count
    citys = list(new_dict.keys())
    values = list(new_dict.values())

    # 下面绘制柱状图
    plt.bar(citys,values)
    plt.xlabel("城市")
    plt.ylabel("岗位数/个")
    plt.title("各城市岗位数量")
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.savefig(path + '/' + "各城市岗位柱状图.jpg")
    plt.show()


def draw_work_experience_pie():
    # 读取爬取的招聘信息表，统计不同城市提供的岗位数量
    f = open('财汇专业招聘岗位信息表.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 创建experience字典
    experience_dict = {}
    for row in rows[1:]:
        if row[6] not in experience_dict:
            experience_dict[row[6]] = 1
        else:
            experience_dict[row[6]] += 1
    # 由于情况较少，可以直接绘图
    labels = list(experience_dict.keys())
    data = list(experience_dict.values())

    # 使用自定义颜色
    colors = ['red', 'pink', 'magenta', 'purple', 'orange']
    # 将横、纵坐标轴标准化处理,保证饼图是一个正圆,否则为椭圆
    plt.axes(aspect='equal')
    # 控制X轴和Y轴的范围(用于控制饼图的圆心、半径)
    plt.xlim(0, 8)
    plt.ylim(0, 8)
    # 不显示边框
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['left'].set_color('none')
    plt.gca().spines['bottom'].set_color('none')
    # 绘制饼图
    plt.pie(x = data,  # 绘制数据
            labels=labels,  # 添加编程语言标签
            colors=colors,  # 设置自定义填充色
            autopct='%.3f%%',  # 设置百分比的格式,保留3位小数
            pctdistance=0.8,  # 设置百分比标签和圆心的距离
            labeldistance=1.0,  # 设置标签和圆心的距离
            startangle=180,  # 设置饼图的初始角度
            center=(4, 4),  # 设置饼图的圆心(相当于X轴和Y轴的范围)
            radius=3.8,  # 设置饼图的半径(相当于X轴和Y轴的范围)
            counterclock=False,  # 是否为逆时针方向,False表示顺时针方向
            wedgeprops={'linewidth': 1, 'edgecolor': 'green'},  # 设置饼图内外边界的属性值
            textprops={'fontsize': 12, 'color': 'black'},  # 设置文本标签的属性值
            frame=1)  # 是否显示饼图的圆圈,1为显示
    # 使中文可以正常显示出来
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 不显示X轴、Y轴的刻度值
    plt.xticks(())
    plt.yticks(())
    # 添加图形标题
    plt.title('财汇专业招聘对工作经验要求')
    plt.savefig(path + '/' + "财汇专业招聘对工作经验要求.jpg")
    # 显示图形
    plt.show()


def draw_education_bar_graph():
    # 读取爬取的招聘信息表，统计不同城市提供的岗位数量
    f = open('财汇专业招聘岗位信息表.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 创建education字典
    education_dict = {}
    for row in rows[1:]:
        if row[7] not in education_dict:
            education_dict[row[7]] = 1
        else:
            education_dict[row[7]] += 1
    # 情况较少，绘制水平条形图
    price = list(education_dict.values())
    keys = list(education_dict.keys())
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 绘图
    plt.barh(range(len(keys)), price, align='center', color='steelblue', alpha=0.8)
    # 添加轴标签
    plt.xlabel('数量')
    # 添加标题
    plt.title('财汇专业对学历要求')
    # 添加刻度标签
    plt.yticks(range(len(keys)), keys)
    # 设置Y轴的刻度范围
    plt.xlim([min(price),max(price)])
    # 为每个条形图添加数值标签
    for x, y in enumerate(price):
        plt.text(y + 0.1, x, '%s' % y, va='center')
    # 显示图形
    plt.savefig(path +'/' +'财汇专业对学历要求.jpg')
    plt.show()


def draw_salary():
    # 相对来说，这个标准较难，我们取前后的平均值
    # 读取爬取的招聘信息表
    f = open('财汇专业招聘岗位信息表.csv', mode='r', encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 计算平均的薪资范围
    first_salary_total = 0
    second_salary_total = 0
    for row in rows[1:]:
        try:
            first_salary = int(row[5].split('-')[0].replace('k',""))
            second_salary = int(row[5].split('-')[1].replace('k',""))
            first_salary_total += first_salary
            second_salary_total += second_salary
        except Exception as error:
            print(error)
    print("统计后财汇专业平均薪资范围是：{:.1f}k——{:.1f}k".format(first_salary_total/len(rows),second_salary_total/len(rows)))


if __name__ == '__main__':
    path = "数据处理图集"
    # 不存在此目录则创建此目录
    if not os.path.exists(path):
        os.mkdir(path)
    draw_city_histogram()
    draw_work_experience_pie()
    draw_education_bar_graph()
    draw_salary()