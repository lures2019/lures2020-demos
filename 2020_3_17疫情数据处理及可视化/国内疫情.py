"""
    由于百度首页的数据信息爬取一星期不是很方便(需要根据百度画的图来提取数据)，于是国内疫情数据选择了[国家卫健委]
    需求：
        1）国家卫健委url网址：http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml
        2）提取页面中3月9号~3月6号的中国、湖北、武汉的相关数据，如下：
            中国：新增确诊病例、新增死亡病例、新增疑似病例、新增治愈出院病例、新增重症病例，接触医学观察的密切接触者
                    现有确诊病例、现有重症病例、累计治愈出院病例、累计死亡病例、累计报告确诊病例、现有疑似病例、累计追踪到的密切接触者、尚在医学观察的密切接触者
            湖北：新增确诊病例、新增治愈出院病例、新增死亡病例、
                现有确诊病例、现有重症病例、累计出院治愈病例、累计死亡病例、累计确诊病例、新增疑似病例、现有疑似病例
            武汉：新增确诊病例、新增治愈出院病例、新增死亡病例、
                现有确诊病例、现有重症病例、累计出院治愈病例、累计死亡病例、累计确诊病例、新增疑似病例、现有疑似病例
        3）将以上数据存储到同一个csv文件中
        4）最后画出中国、湖北、武汉的折线图
"""
import csv
import os
import matplotlib.pyplot as plt

# 国家卫健委官网：http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml反扒机制过强，未找到合适的途径(selenium同样未解决)
# 因为是爬取上个星期即3月9号~3月16号的数据，于是直接提取网址，进行爬取分析,cookie经常失效，未找到合适办法
# 将中国、湖北、武汉近一星期的数据写入csv文件中

def get_China_new_add(path):
    path1 = path + '/' + '中国新增数据'
    if not os.path.exists(path1):
        os.mkdir(path1)
    f = open(path1 + '/' + '中国近一星期新增数据.csv', mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['日期', '中国新增确诊病例', '中国新增死亡病例', '中国新增疑似病例', '新增治愈出院病例', '解除医学观察的密切接触者', '减少重症病例'])

    # 数据来源于国家卫建委，真实有效
    # 只有国家卫建委拥有多天数据记录，腾讯、百度首页、搜狐、网易等只拥有当天数据记录！
    date = ['3月9号', '3月10号', '3月11号', '3月12号', '3月13号', '3月14号', '3月15号','3月16号']
    new_diagnose = [19, 24, 15, 8, 11, 20, 16,21]          # 新增确诊
    new_death = [17, 22, 11, 7, 13, 10, 14,13]             # 新增死亡
    new_might = [36, 31, 33, 33, 17, 39, 41,45]            # 新增疑似

    # 后面三组数据不宜和前面3组在一起画图，因为数量级相差太大，会导致前面的数据没有意义
    new_out = [1297, 1578, 1318, 1318, 1430, 1370, 838,930]         # 新增治愈出院
    new_person = [4148, 3235, 2206, 2483, 2714, 1409, 1316,1105]     # 新增解除医学观察的密切接触者
    new_serious = [317, 302, 235, 237, 410, 384, 194,202]           # 减少的重症病例
    # 保存数据到csv文件中
    for i in range(len(date)):
        csv_write.writerow([date[i], new_diagnose[i], new_death[i], new_might[i], new_out[i], new_person[i], new_serious[i]])
    f.close()

    # Python画折线图
    # Python画中国新增确诊、疑似、死亡病例折线图
    plt.plot(date, new_diagnose, label='中国新增确诊病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, new_death, label='中国新增死亡病例')
    plt.plot(date, new_might, label='中国新增疑似病例')
    plt.xlabel('日期')
    plt.ylabel('新增人数')
    plt.title('中国近一星期新增数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path1 + '/' + '中国新增确诊_死亡_疑似病例折线图.jpg')
    plt.show()

    # Python画新增治愈、解除医院观察的密切接触者、减少的重症病例折线图
    plt.plot(date, new_out, label='中国新增治愈出院病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, new_person, label='新增解除医院观察的密切接触者')
    plt.plot(date, new_serious, label='减少的重症病例')
    plt.xlabel('日期')
    plt.ylabel('新增人数')
    plt.title('中国近一星期新增数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path1 + '/' + '中国新增治愈出院_解除医院观察的密切接触者_减少的重症病例.jpg')
    plt.show()


    # 数据来源于国家卫健委，真实有效
    # 下面列表中的数据是现有的相关病例数据以及累计的数据
    path2 = path + '/' + '中国现有数据'
    if not os.path.exists(path2):
        os.mkdir(path2)
    f2 = open(path2 + '/' + '中国近一星期所有数据.csv', mode="w", newline='', encoding="utf-8-sig")
    csv_write2 = csv.writer(f2)
    csv_write2.writerow(['日期','现有确诊病例', '现有重症病例', '累计治愈出院病例', '累计死亡病例', '累计报告确诊病例', '现有疑似病例', '累计追踪到密切接触者', '尚在医学观察的密切接触者'])
    now_diagnose = [17721,16145,14831,13526,12094,10734,9898,8976]           # 现有确诊
    now_serious = [4794,4492,4257,4020,3610,3226,3032,2830]            # 现有重症
    sum_death = [3136,3158,3169,3176,3189,3199,3213,3226]              # 累计死亡病例

    sum_out = [59897,61475,62793,64111,65541,66911,67749,68679]                # 累计治愈出院病例
    sum_diagnose = [80754,80778,80793,80813,80824,80844,80860,80881]           # 累计报告确诊病例
    now_in = [16982,14607,13701,12161,10879,10189,9582,9351]                 # 尚在医学观察的密切接触者

    now_might = [349,285,253,147,115,113,134,128]              # 现有疑似病例
    sum_person = [675338,675886,677243,678088,678935,679759,680462,681404]             # 累计追踪到的密切接触者

    for j in range(len(now_diagnose)):
        csv_write2.writerow([date[j],now_diagnose[j],now_serious[j],sum_out[j],sum_death[j],sum_diagnose[j],now_might[j],sum_person[j],now_in[j]])
    f2.close()

    # Python画折线图
    # Python画中国累计治愈出院、累计报告确诊、尚在医学观察的密切接触者病例折线图
    plt.plot(date, sum_out, label='中国累计治愈出院病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, sum_diagnose, label='累计报告确诊病例')
    plt.plot(date, now_in, label='尚在医学观察的密切接触者')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('中国近一星期所有数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path2 + '/' + '中国累计治愈出院_累计报告确诊_尚在医学观察的密切接触者折线图.jpg')
    plt.show()

    # Python画折线图
    # Python画中国现有确诊、现有重症、累计死亡病例折线图
    plt.plot(date, now_diagnose, label='中国现有确诊病例', linewidth=3, color='r', marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(date, now_serious, label='中国重症病例')
    plt.plot(date, sum_death, label='累计死亡病例')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('中国近一星期所有数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path2 + '/' + '中国现有确诊_重症_累计死亡病例折线图.jpg')
    plt.show()




def get_hubei_add(path):
    path1 = path + '/' + '湖北新增数据'
    if not os.path.exists(path1):
        os.mkdir(path1)
    f = open(path1 + '/' + '湖北近一星期新增数据.csv', mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['日期', '湖北新增确诊病例', '湖北新增死亡病例', '湖北新增疑似病例', '湖北治愈出院病例'])

    # 数据来源于国家卫建委，真实有效
    # 只有国家卫建委拥有多天数据记录，腾讯、百度首页、搜狐、网易等只拥有当天数据记录！
    date = ['3月9号', '3月10号', '3月11号', '3月12号', '3月13号', '3月14号', '3月15号','3月16号']
    new_diagnose = [17, 13, 8, 5, 4, 4, 4,1]          # 新增确诊
    new_death = [17, 22, 10, 6, 13, 10, 14,12]             # 新增死亡
    new_might = [13, 6, 2, 1, 0, 1, 2,0]            # 新增疑似

    # 后面三组数据不宜和前面3组在一起画图，因为数量级相差太大，会导致前面的数据没有意义
    new_out = [1152, 1471, 1242, 1255, 1390, 1335, 816,893]     # 新增治愈出院
    # 保存数据到csv文件中
    for i in range(len(date)):
        csv_write.writerow([date[i], new_diagnose[i], new_death[i], new_might[i], new_out[i]])
    f.close()

    # Python画折线图
    # Python画中国新增确诊、疑似、死亡病例折线图
    plt.plot(date, new_diagnose, label='湖北新增确诊病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, new_death, label='湖北新增死亡病例')
    plt.plot(date, new_might, label='湖北新增疑似病例')
    plt.xlabel('日期')
    plt.ylabel('新增人数')
    plt.title('湖北近一星期新增数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path1 + '/' + '湖北新增确诊_死亡_疑似病例折线图.jpg')
    plt.show()

    # 以下数据来源于国家卫建委，绝对真实有效
    # 下面是湖北现存病例数据
    path2 = path + '/' + '湖北现有数据'
    if not os.path.exists(path2):
        os.mkdir(path2)
    f2 = open(path2 + '/' + '湖北近一星期所有数据.csv', mode="w", newline='', encoding="utf-8-sig")
    csv_write2 = csv.writer(f2)
    csv_write2.writerow(['日期','现有确诊病例','现有重症病例','累计治愈出院病例','累计死亡病例','累计确诊病例','现有疑似病例'])
    now_diagnose = [17151,15671,14427,13171,11772,10431,9605,8701]           # 现有确诊病例
    now_serious = [4701,4412,4180,3948,3543,3163,2975,2782]            # 现有重症
    sum_death = [3024,3046,3056,3062,3075,3085,3099,3111]              # 累计死亡病例

    sum_out = [47585,49056,50298,51553,52943,54278,55094,55987]                # 累计治愈出院病例
    sum_diagnose = [67760,67773,67781,67786,67790,67794,67798,67799]           # 累计确诊病例
    now_migtht = [246,198,158,49,34,18,18,3]             # 现有疑似病例

    for j in range(len(now_diagnose)):
        csv_write2.writerow([date[j],now_diagnose[j],now_serious[j],sum_out[j],sum_death[j],sum_diagnose[j],now_migtht[j]])
    f2.close()

    # Python画折线图
    # Python画湖北累计治愈出院、累计报告确诊病例折线图
    plt.plot(date, sum_out, label='湖北累计治愈出院病例', linewidth=3, color='r', marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(date, sum_diagnose, label='累计报告确诊病例')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('湖北近一星期所有数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path2 + '/' + '湖北累计治愈出院_累计报告确诊病例折线图.jpg')
    plt.show()

    # Python画折线图
    # Python画湖北现有确诊、现有重症、累计死亡病例折线图
    plt.plot(date, now_diagnose, label='湖北现有确诊病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, now_serious, label='湖北重症病例')
    plt.plot(date, sum_death, label='累计死亡病例')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('湖北近一星期所有数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path2 + '/' + '湖北现有确诊_重症_累计死亡病例折线图.jpg')
    plt.show()






def get_wuhan_add(path):
    path1 = path + '/' + '武汉新增数据'
    if not os.path.exists(path1):
        os.mkdir(path1)
    f = open(path1 + '/' + '武汉近一星期新增数据.csv', mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['日期', '武汉新增确诊病例', '武汉新增死亡病例', '武汉新增疑似病例', '武汉治愈出院病例'])

    # 数据来源于国家卫建委，真实有效
    # 只有国家卫建委拥有多天数据记录，腾讯、百度首页、搜狐、网易等只拥有当天数据记录！
    date = ['3月9号', '3月10号', '3月11号', '3月12号', '3月13号', '3月14号', '3月15号','3月16号']
    new_diagnose = [17, 13, 8, 5, 4, 4, 4,1]      # 新增确诊
    new_death = [16, 19, 7, 6, 10, 10, 13,11]         # 新增死亡
    new_might = [12, 6, 2, 1, 0, 1, 2,0]        # 新增疑似

    # 后面三组数据不宜和前面3组在一起画图，因为数量级相差太大，会导致前面的数据没有意义
    new_out = [896, 1212, 1053, 1103, 1254, 1181, 752,836]     # 新增治愈出院
    # 保存数据到csv文件中
    for i in range(len(date)):
        csv_write.writerow([date[i], new_diagnose[i], new_death[i], new_might[i], new_out[i]])
    f.close()

    # Python画折线图
    # Python画中国新增确诊、疑似、死亡病例折线图
    plt.plot(date, new_diagnose, label='武汉新增确诊病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, new_death, label='武汉新增死亡病例')
    plt.plot(date, new_might, label='武汉新增疑似病例')
    plt.xlabel('日期')
    plt.ylabel('新增人数')
    plt.title('武汉近一星期新增数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path1 + '/' + '武汉新增确诊_死亡_疑似病例折线图.jpg')
    plt.show()

    # 以下数据来源于国家卫建委，绝对真实有效
    # 下面是武汉现存病例数据
    path2 = path + '/' + '武汉现有数据'
    if not os.path.exists(path2):
        os.mkdir(path2)
    f2 = open(path2 + '/' + '武汉近一星期所有数据.csv', mode="w", newline='', encoding="utf-8-sig")
    csv_write2 = csv.writer(f2)
    csv_write2.writerow(['日期', '现有确诊病例', '现有重症病例', '累计治愈出院病例', '累计死亡病例', '累计确诊病例','现有疑似病例'])
    now_diagnose = [15732,14514,13462,12358,11098,9911,9150,8304]  # 现有确诊病例
    now_serious = [4471,4217,4003,3793,3410,3058,2878,2695]  # 现有重症
    sum_out = [31829,33041,34094,35197,36451,37632,38384,55987]  # 累计治愈出院病例
    sum_death = [2404,2423,2430,2436,2446,2456,2469,2480]  # 累计死亡病例
    sum_diagnose = [49965,49978,49986,49991,49995,49999,50003,67799]  # 累计确诊病例
    now_might = [230,192,152,44,30,15,15,1]          #现有疑似病例

    for j in range(len(now_diagnose)):
        csv_write2.writerow([date[j],now_diagnose[j],now_serious[j],sum_out[j],sum_death[j],sum_diagnose[j],now_might[j]])
    f2.close()
    # Python画折线图
    # Python画武汉累计治愈出院、累计报告确诊病例折线图
    plt.plot(date, sum_out, label='武汉累计治愈出院病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, sum_diagnose, label='累计报告确诊病例')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('武汉近一星期所有数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path2 + '/' + '武汉累计治愈出院_累计报告确诊病例折线图.jpg')
    plt.show()

    # Python画折线图
    # Python画武汉现有确诊、现有重症、累计死亡病例折线图
    plt.plot(date, now_diagnose, label='武汉现有确诊病例', linewidth=3, color='r', marker='o', markerfacecolor='blue',markersize=12)
    plt.plot(date, now_serious, label='武汉重症病例')
    plt.plot(date, sum_death, label='累计死亡病例')
    plt.xlabel('日期')
    plt.ylabel('目前人数')
    plt.title('武汉近一星期所有数据')
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path2 + '/' + '武汉现有确诊_重症_累计死亡病例折线图.jpg')
    plt.show()


if __name__ == '__main__':
    path = '国内疫情数据'
    # 判断是否具有此目录，无则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    get_China_new_add(path)
    get_hubei_add(path)
    get_wuhan_add(path)
