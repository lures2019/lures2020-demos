# Python批量爬取BiliBili排行版100的所有视频以及弹幕
"""
    后期需要完善：
        1）做出GUI界面
        2）添加批量下载某个博主或者某个链接下的所有视频
        3）下载一个单独的视频
        4）手动添加下载路径
        5)界面卡死的问题
        6）添加log/about等菜单项
"""
import requests
import parsel
import datetime
import csv
import os
import you_get
import sys
import tkinter
from PIL import Image,ImageTk
from tkinter import messagebox
import threading

# 1、开始分析排行版网页，提取出所有的视频链接
def analyse_html(imock):
    url = 'https://www.bilibili.com/v/popular/rank/all?spm_id_from=333.851.b_7072696d61727950616765546162.3'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    # print(response.text)

    # 经过网页的分析后，发现所有的视频都以<li></li>形式存放在<ul class="rank-list">里面，所有可以开始用CSS选择器进行第一层提取
    select = parsel.Selector(response.text)
    lis = select.css('ul.rank-list li').getall()

    # 开始进行第二层提取，建立多个变量分别存取多个有用信息
    ranks = []
    videos = []
    video_names = []
    video_watch_numbers = []
    video_barrage_numbers = []
    video_labels = []
    video_scores = []

    for i in range(len(lis)):
        select_now = parsel.Selector(lis[i])
        # 提取排行版排名
        rank = int(select_now.css('li::attr(data-rank)').get())
        ranks.append(rank)
        # 提取视频链接
        video = 'https:' + str(select_now.css('.info > a::attr(href)').get())
        videos.append(video)
        # 提取视频标题
        video_name = select_now.css('.info > a::text').get()
        video_names.append(video_name)
        # 提取视频播放量数据,strip()是去除空行
        video_watch_number = select_now.css('.info > .detail span.data-box::text').getall()[0].strip()
        video_watch_numbers.append(video_watch_number)
        # 提取弹幕数量
        video_barrage_number = select_now.css('.info > .detail span.data-box::text').getall()[1].strip()
        video_barrage_numbers.append(video_barrage_number)
        # 提取视频标签
        video_label = select_now.css('.info > .detail > a span ::text').get().strip()
        video_labels.append(video_label)
        # 提取综合评分,此处转为int的话，会超出范围
        video_score = select_now.css('.info > .pts div::text').get()
        video_scores.append(video_score)
    # 返回几个变量列表,这样操作可以减少空间
    if imock == 1:
        return videos,video_names
    else:
        return ranks,videos,video_names,video_watch_numbers,video_barrage_numbers,video_labels,video_scores



# 2、将一些信息存放到以   日期+事件形式命名的csv文件中
def write_data_to_csv():
    time = str(datetime.datetime.now()).split(' ')[0]
    ranks, videos, video_names, video_watch_numbers, video_barrage_numbers, video_labels, video_scores = analyse_html(0)
    f = open(path + '/' + '{}.csv'.format(time),mode='w+',newline="",encoding='utf-8-sig')
    csv_write = csv.writer(f)
    csv_write.writerow(['排行','链接','名称','播放量','弹幕量','标签','综合评分'])
    for i in range(len(ranks)):
        csv_write.writerow([ranks[i],videos[i],video_names[i],video_watch_numbers[i],video_barrage_numbers[i],video_labels[i],video_scores[i]])
    f.close()



# 3、设置视频下载模式相关信息
def download_videos(path_now,url):
    # 调用指令,-o 是指令的参数，sys操纵系统模块
    sys.argv = ['you-get','-o',path_now,url]
    # 默认下载是flv格式
    you_get.main()

# 4、开始下载视频
def ExtracVideo():
    videos,video_names = analyse_html(1)
    time = str(datetime.datetime.now()).split(' ')[0]
    path_now = time
    if not os.path.exists(path + '/' + path_now):
        os.mkdir(path + '/' + path_now)
    for url in videos:
        download_videos(path + '/' + path_now,url)





# 6、单个视频提取原则,获取用户输入的url
def download_one_video():
    # 获取用户输入的结果
    content = entry1.get()
    # 去除多余的空格，用于判断用户手输入了信息！
    con = content.strip()
    if con == "":
        messagebox.showinfo('提示', '请输入要下载的视频链接!')
    else:
        time = str(datetime.datetime.now()).split(' ')[0]
        path_now = time
        if not os.path.exists(path + '/' + path_now):
            os.mkdir(path + '/' + path_now)
        download_videos(path + '/' + path_now,con)


# 7、开始下载BiliBili某up主所有视频集合
def download_study_videos():
    # 获取用户输入的结果
    content = entry2.get()
    # 去除多余的空格，用于判断用户手输入了信息！
    con = str(content.strip().split('?')[0])
    if con == "":
        messagebox.showinfo('提示', '请输入要下载的视频链接!')
    else:
        time = str(datetime.datetime.now()).split(' ')[0]
        path_now = time
        if not os.path.exists(path + '/' + path_now):
            os.mkdir(path + '/' + path_now)
        response = requests.get(url=con)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        page = select.xpath('//div[@id="multi_page"]/div[@class="head-con"]/div[@class="range-box"]/span/text()').get()
        pages = int(str(page).split('/')[-1])
        for page in range(pages):
            con_now = con + "?p={}".format(page)
            download_videos(path + '/' + path_now, con_now)

# 8、开多线程
def thread_it(func):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()

# 9、添加About介绍菜单
def about():
    messagebox.showinfo('提示', '本应用写于2020年11月1日，制作人lures！')


# 主函数部分
if __name__ == '__main__':
    path = 'BiliBili排行版信息'
    # 如果此文件夹不存在就创建一下此文件夹
    if not os.path.exists(path):
        os.mkdir(path)
    # write_data_to_csv()
    # ExtracVideo()
    # 5、添加GUI界面
    top = tkinter.Tk()
    top.title('BiliBili视频下载小工具')
    width = 500
    height = 655
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = top.winfo_screenwidth()
    screenheight = top.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    top.geometry(alignstr)
    top.resizable(0, 0)
    # 添加button控件
    # 都添加一些控件，来占行，使得界面好看一点
    # 不支持png等格式，需要先用pillow处理
    img = Image.open('背景图片_gaitubao_500x300.png')
    photo = ImageTk.PhotoImage(img)
    theLable = tkinter.Label(top, text="微信公众号,\n空谷小莜蓝",  # 内容
                             justify=tkinter.CENTER,  # 对齐方式
                             image=photo,  # 加入图片
                             compound=tkinter.CENTER,  # 关键：设置为背景图片
                             font=("华文行楷", 20),  # 字体和字号
                             fg='white',
                             width=500,
                             height=500)  # 前景色
    theLable.grid(row=0, column=0, rowspan=2, columnspan=2)
    label1 = tkinter.Label(top, text="单个BiliBili视频链接：", width='20')
    label1.grid(row=3, column=0)
    entry1 = tkinter.Entry(top, font=("仿宋", 12), width='35')
    entry1.grid(row=3, column=1)
    label2 = tkinter.Label(top, text="BiliBili网课批量下载：", width='20')
    label2.grid(row=4, column=0)
    entry2 = tkinter.Entry(top, font=("仿宋", 12), width='35')
    entry2.grid(row=4, column=1)
    text1 = tkinter.Label(top, width='30').grid(row=5, column=0)
    text2 = tkinter.Label(top, width='30').grid(row=5, column=1)
    button1 = tkinter.Button(top, text="排行版100", width="30", command=lambda :thread_it(ExtracVideo))
    button1.grid(row=6, column=0)
    button2 = tkinter.Button(top, text='单个视频', width='30',command=lambda :thread_it(download_one_video))
    button2.grid(row=6, column=1,sticky='e')
    button3 = tkinter.Button(top, text='网课系列视频', width='30',command=lambda :thread_it(download_study_videos))
    button3.grid(row=7, column=0)
    button4 = tkinter.Button(top, text='退出', width='30',command=top.quit)
    button4.grid(row=7, column=1,sticky='e')
    label3 = tkinter.Label(top, text="lures友情出品！欢迎致电2142781703~~~").grid(row=8, column=1)
    menu1 = tkinter.Menu(top)
    menu1.add_command(label="About",command=about)
    top.config(menu=menu1)
    # 设置窗口图标
    top.iconbitmap('logo.ico')
    top.mainloop()






