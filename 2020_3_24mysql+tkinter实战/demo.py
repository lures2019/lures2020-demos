from tkinter import *
from tkinter import messagebox


"""
    需求：
        就是设计一个爬虫，给功能如下，
        1.抓取网页上关于光电企业信息（岗位，各岗位的薪资、技能要求、工资、地点等信息）
        2.将这些信息存入数据库
        3.对数据库的数据进一步分析，提炼，并将信息转换为散点图和柱状图，并加入了tkinter图形操作界面
"""
import requests
import pymysql
import matplotlib.pyplot as plot
import re

# 1.1、先爬取拉勾的数据,是一个ajax动态加载的网站
headers = {
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E5%85%89%E7%94%B5?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
def get_lagou_cookie():
    # 原始网页的URL
    url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
    s = requests.Session()
    s.get(url, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    return cookie


def get_salary_from_mysql():
    # 获取薪资
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        database='position_message',
        user='root',
        password='wangzhi20001115', charset='utf8')
    cs1 = connection.cursor()
    sql1 = "select salary from lagou "
    cs1.execute(sql1)
    datalist = []
    alldata = cs1.fetchall()
    for s in alldata:
        datalist.append(s[0])
    return datalist

def get_workYear_from_mysql():
    # 获取工作经验
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        database='position_message',
        user='root',
        password='wangzhi20001115', charset='utf8')
    cs1 = connection.cursor()
    sql1 = "select workYear from lagou "
    cs1.execute(sql1)
    datalist = []
    alldata = cs1.fetchall()
    for s in alldata:
        datalist.append(s[0])
    return datalist

def paint_pie_chart_of_salary():
    salary = get_salary_from_mysql()
    labels = ['1k-10k','11k-20k','21k-30k','31k-100k']
    s1 = s2 = s3 = s4 = 0
    for i in range(len(salary)):
        result = re.findall('(.*?)k-(.*?)k',salary[i])
        for x,y in result:
            end = (int(x)+int(y))/2
            if(1<end<=10):
                s1 += 1
            elif(end<=20):
                s2 += 1
            elif(end<=30):
                s3 += 1
            else:
                s4 += 1
    sizes = [s1,s2,s3,s4]
    colors = ['red','yellow','blue','green']
    explode = (0.05,0,0,0)
    patches, l_text, p_text = plot.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       labeldistance=1.1, autopct='%2.0f%%', shadow=False,
                                       startangle=90, pctdistance=0.6)
    for t in l_text:
        t.set_size = 30
    for t in p_text:
        t.set_size = 20
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plot.axis('equal')
    plot.title("薪资分布饼状图")
    plot.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
    # 显示中文名称
    plot.rcParams['font.sans-serif'] = ['SimHei']
    plot.rcParams['axes.unicode_minus'] = False
    plot.legend()
    plot.savefig('薪资分布饼状图.jpg')
    plot.show()

def paint_pie_chart_of_workYear():
    workYear = get_workYear_from_mysql()
    labels = ['1-3年', '3-5年', '5-10年', '应届毕业生','不限']
    w1 = w2 = w3 = w4 = w5 = 0
    for i in range(len(workYear)):
        if(workYear[i] == '1-3年'):
            w1 += 1
        elif(workYear[i] == '3-5年'):
            w2 += 1
        elif(workYear[i] == '5-10年'):
            w3 += 1
        elif(workYear[i] == '应届毕业生'):
            w4 += 1
        else:
            w5 += 1
    sizes = [w1, w2, w3, w4,w5]
    colors = ['red', 'yellow', 'blue', 'green','purple']
    explode = (0.05, 0, 0, 0,0)
    patches, l_text, p_text = plot.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       labeldistance=1.1, autopct='%2.0f%%', shadow=False,
                                       startangle=90, pctdistance=0.6)
    for t in l_text:
        t.set_size = 30
    for t in p_text:
        t.set_size = 20
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plot.axis('equal')
    plot.title("工作经验分布饼状图")
    plot.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
    # 显示中文名称
    plot.rcParams['font.sans-serif'] = ['SimHei']
    plot.rcParams['axes.unicode_minus'] = False
    plot.legend()
    plot.savefig('工作经验分布饼状图.jpg')
    plot.show()

def paint_bar_chart_of_salary():
    salary = get_salary_from_mysql()
    labels = ['1k-10k','11k-20k','21k-30k','31k-100k']
    s1 = s2 = s3 = s4 = 0
    for i in range(len(salary)):
        result = re.findall('(.*?)k-(.*?)k',salary[i])
        for x,y in result:
            end = (int(x)+int(y))/2
            if(1<end<=10):
                s1 += 1
            elif(end<=20):
                s2 += 1
            elif(end<=30):
                s3 += 1
            else:
                s4 += 1
    sizes = [s1,s2,s3,s4]
    plot.bar(range(len(sizes)),sizes,color="rgb",tick_label=labels)
    plot.title("薪资分布柱状图")
    # 显示中文名称
    plot.rcParams['font.sans-serif'] = ['SimHei']
    plot.rcParams['axes.unicode_minus'] = False
    plot.savefig('薪资分布柱状图.jpg')
    plot.show()

def paint_bar_chart_of_workYear():
    workYear = get_workYear_from_mysql()
    labels = ['1-3年', '3-5年', '5-10年', '应届毕业生','不限']
    w1 = w2 = w3 = w4 = w5 = 0
    for i in range(len(workYear)):
        if(workYear[i] == '1-3年'):
            w1 += 1
        elif(workYear[i] == '3-5年'):
            w2 += 1
        elif(workYear[i] == '5-10年'):
            w3 += 1
        elif(workYear[i] == '应届毕业生'):
            w4 += 1
        else:
            w5 += 1
    sizes = [w1, w2, w3, w4,w5]
    plot.bar(range(len(sizes)), sizes, color="rgb", tick_label=labels)
    plot.title("工作经验分布柱状图")
    # 显示中文名称
    plot.rcParams['font.sans-serif'] = ['SimHei']
    plot.rcParams['axes.unicode_minus'] = False
    plot.savefig('工作经验分布柱状图.jpg')
    plot.show()



def main():
    url1 = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    # 获取用户输入的结果
    content = entry.get()
    # 去除多余的空格，用于判断用户手输入了信息！
    con = content.strip()
    if con == "":
        messagebox.showinfo('提示', '请输入要翻译的内容!')
    else:
        for i in range(int(10)):
            json = {
                'first': 'true',
                'pn': str(i),
                'kd': content
            }
            response = requests.post(url=url1, headers=headers, data=json, cookies=get_lagou_cookie())
            response.encoding = response.apparent_encoding
            html = response.json()['content']['positionResult']['result']
            data = [[] for i in range(len(html))]
            # 连接数据库
            connection = pymysql.connect(
                host='localhost',  # 服务器的ip
                port=3306,  # 数据库开发的端口
                user='root',  # 用户名
                password='wangzhi20001115',  # 密码
                database='position_message',  # 需要使用的数据库
            )
            # 获取执行命令的游标
            cursor = connection.cursor()
            for i in range(len(html)):
                data[i].append(str(html[i]['positionName']))  # 职位名称
                data[i].append(str(html[i]['companyFullName']))  # 公司全名
                data[i].append(str(html[i]['companySize']))  # 公司规模
                data[i].append(str(html[i]['financeStage']))  # 是否融资
                data[i].append(str(html[i]['positionAdvantage']))  # 公司福利
                data[i].append(str(html[i]['positionLables']))  # 能力要求
                data[i].append(str(html[i]['createTime']))  # 发布时间
                data[i].append(str(html[i]['city'] + html[i]['district']))  # 具体的地址
                data[i].append(str(html[i]['salary']))  # 薪资
                data[i].append(str(html[i]['workYear']))  # 工作经验
                data[i].append(str(html[i]['education']))  # 学历要求
            for d in data:
                cursor.execute(
                    'insert into lagou(positionName, companyFullName, companySize,financeStage,positionAdvantage,positionLables,createTime,location,salary,workYear,education) values (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)',
                    d)
            connection.commit()  # 提交修改
            cursor.close()  # 关闭游标 关闭链接
            connection.close()
            result1.set("第{}页数据保存到数据库position_message的数据表lagou中".format(str(i)))
        print("下面开始从数据库中读取数据！")
        paint_pie_chart_of_salary()
        paint_pie_chart_of_workYear()
        paint_bar_chart_of_salary()
        paint_bar_chart_of_workYear()






window = Tk()
window.geometry('335x100+600+300')
window.resizable(0,0)
window.title('招聘信息下载器')

# 控件
label = Label(window,text="请输入要爬取的职位：",font=("仿宋",12))
label.grid(row=0,column=0,sticky='e')

entry = Entry(window,font=("仿宋",12))
entry.grid(row=0,column=1)

label1 = Label(window,text="当前正在爬取的情况：",font=("仿宋",12))
label1.grid(row=1,column=0,sticky='e')
# 随时变化的量
result1 = StringVar()
entry1 = Entry(window,font=("仿宋",12),textvariable=result1)
entry1.grid(row=1,column=1)

# 空出一行,使布局漂亮些
label2 = Label(window, text="")
label2.grid(row=2, column=0)
# 按钮
button = Button(window, text="开始爬取", width="10",command=main)
button.grid(row=3, column=0, sticky='w')
# command = window.quit是用来退出界面的！
button1 = Button(window, text="退出", width="10", command=window.quit)
button1.grid(row=3, column=1, sticky='e')
# 显示窗口(消息循环)
window.mainloop()

main()