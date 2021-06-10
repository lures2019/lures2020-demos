import requests
import os
import parsel
import jieba
import cv2
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tkinter
from tkinter import messagebox
import threading



# function 1.1————Get layout lists
def get_layout_lists(url):
    response = requests.get(url)
    # 设置万能解码
    response.encoding = response.apparent_encoding
    # 使用xpath进行网页解析
    select = parsel.Selector(response.text)
    # 版面下级主题链接
    links = select.xpath('//section[@id="body"]/div[@class="b-content corner"]/table/tbody/tr/td[@class="title_1"]/a/@href').getall()
    # 构造真实链接
    real_links = ['https://www.newsmth.net/nForum/#!' + i.split('/nForum/')[-1] for i in links]

    return real_links


# function 1.2————Get specific information,获取的是每个讨论区的话题前十
def get_specific_information(url):
    real_links = get_layout_lists(url)
    # 构建大列表进行存储
    top_topic = []
    # 存储发帖用户及其发帖数
    authors = []
    # 开始对链接进行遍历
    for link in real_links:
        try:
            new_url = 'https://www.newsmth.net/nForum/' + link.split('/#!')[-1] + '?ajax'
            response = requests.get(new_url)
            response.encoding = response.apparent_encoding
            select = parsel.Selector(response.text)
            # 提取出页数,从这可以区分二级目录和普通的版块,二级目录显示None
            page = select.xpath('//section[@id="body"]/div[4]/div[1]/ul/li[1]/i/text()').get()
            if page == None:
                print(new_url)
                response = requests.get(new_url)
                response.encoding = response.apparent_encoding
                select = parsel.Selector(response.text)
                my_links = select.xpath('//section[@id="body"]/div[2]/table/tbody/tr/td[1]/a/@href').getall()
                # 开始遍历筛选
                for end_link in my_links:
                    end_url = 'https://www.newsmth.net' + end_link + '?ajax'
                    response = requests.get(end_url)
                    response.encoding = response.apparent_encoding
                    select = parsel.Selector(response.text)
                    # 提取出页数,从这可以区分二级目录和普通的版块,二级目录显示None
                    page = select.xpath('//section[@id="body"]/div[4]/div[1]/ul/li[1]/i/text()').get()
                    my_dict = {
                        'topic': [],
                        'nums': []
                    }
                    author_dict = {}
                    # for i in range(1,int(page) + 1):
                    for i in range(1, 11):
                        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
                        url_end = end_url + '&p={}'.format(i)
                        response = requests.get(url_end)
                        response.encoding = response.apparent_encoding
                        select = parsel.Selector(response.text)
                        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
                        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
                        for info in info_range:
                            reply_time = info.xpath('./td[8]/a/text()').get()
                            # 筛选出是2021年的,注意是字符串
                            if reply_time.split('-')[0] == '2021':
                                # 筛选出话题名称和回复数
                                topic = info.xpath('./td[2]/a/text()').get()
                                reply_nums = info.xpath('./td[7]/text()').get()
                                author = info.xpath('./td[4]/a/text()').get()

                                my_dict['topic'].append(topic)
                                my_dict['nums'].append(int(reply_nums))
                                if author not in author_dict:
                                    author_dict[author] = 1
                                else:
                                    author_dict[author] += 1
                    # my_dict筛选得到信息添加到大列表中
                    top_topic.append(my_dict)
                    authors.append(author_dict)
                    print(my_dict)
            else:
                # 页面构成规则类似https://www.newsmth.net/nForum/board/XDU?ajax&p=2，即p后面的数字代表当前页
                # 新建一个字典存储各个主题名称以及回复数
                my_dict = {
                    'topic':[],
                    'nums':[]
                }
                author_dict = {}
                # for i in range(1,int(page) + 1):
                for i in range(1,11):
                    # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
                    url_end = new_url + '&p={}'.format(i)
                    response = requests.get(url_end)
                    response.encoding = response.apparent_encoding
                    select = parsel.Selector(response.text)
                    # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
                    info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
                    for info in info_range:
                        reply_time = info.xpath('./td[8]/a/text()').get()
                        # 筛选出是2021年的,注意是字符串
                        if reply_time.split('-')[0] == '2021':
                            # 筛选出话题名称和回复数
                            topic = info.xpath('./td[2]/a/text()').get()
                            reply_nums = info.xpath('./td[7]/text()').get()
                            author = info.xpath('./td[4]/a/text()').get()

                            my_dict['topic'].append(topic)
                            my_dict['nums'].append(int(reply_nums))
                            if author not in author_dict:
                                author_dict[author] = 1
                            else:
                                author_dict[author] += 1
                # my_dict筛选得到信息添加到大列表中
                top_topic.append(my_dict)
                authors.append(author_dict)
                print(my_dict)
        except Exception as error:
            print(error)
    # 开始对top_topic进行处理
    scores = []
    for mess in top_topic:
        mess_scores = list(mess['nums'])
        for score in mess_scores:
            scores.append(score)
    # 对scores进行排序，筛选出排名第10的分数
    limit_score = sorted(scores,reverse=True)[9]
    scores_ret = sorted(scores,reverse=True)[:10]
    topics = []
    try:
        for mess in top_topic:
            nums = list(mess['nums'])
            topic_now = list(mess['topic'])
            for i in range(len(nums)):
                if int(nums[i]) >= limit_score:
                    topics.append(topic_now[i])
    except Exception as error:
        print(error,top_topic)
    # 对发帖用户列表进行处理
    authors_end = []
    values_end = []
    for i in range(len(authors)):
        # 找到每一个字典的value的最大值
        max_value = max(list(authors[i].values()))
        for key,value in authors[i].items():
            if value == max_value:
                authors_end.append(key)
                values_end.append(value)
            else:
                pass
    # 输出列表中最大的发帖用户以及分数
    value_now = max(values_end)
    for i in range(len(authors_end)):
        if values_end[i] == value_now:
            print("❤❤❤❤❤❤❤❤❤❤当前讨论区发言最多的账户id是{},发帖数是{}❤❤❤❤❤❤❤❤❤❤".format(authors_end[i],values_end[i]))
            break
    return scores_ret,topics


# function 1.3————Information Integration
def information_integration():
    topics_total = []
    scores_total = []
    # 创建讨论区名称列表
    names = ['国内院校','休闲娱乐','五湖四海','游戏运动','社会信息','知性感性','文化人文','学术科学','电脑技术']
    # i的范围就是几个版块
    for i in range(1,10):
        url = 'https://www.newsmth.net/nForum/section/{}?ajax'.format(i)
        try:
            scores_ret, topics = get_specific_information(url)
            # 将所有信息都存放进列表，用于实现功能2
            topics_total.append(list(topics))
            scores_total.append(scores_ret)
        except Exception as e:
            print(e)
    # 获取总体的最高分
    end_scores = []
    end_topics = []
    for scores in scores_total:
        for score in scores:
            end_scores.append(score)
    limit_score = sorted(end_scores,reverse=True)[9]
    for i in range(len(scores_total)):
        for j in range(len(scores_total[0])):
            if scores_total[i][j] >= limit_score:
                end_topics.append(topics_total[i][j])
    return end_topics,names,topics_total



# function 1.4————Draw wordcloud picture and save information
def draw_wordcloud():
    topics,names,topics_total = information_integration()
    # 去除一些id
    words = "".join(topics).replace("转载","").replace("完结","").replace("Re","").replace("已完本","").replace("暗夜将至","")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path = " C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color = 'white',
        # 词云形状
        mask = color_mask,
        # 允许最大词汇
        max_words = 500,
        # 最大号字体
        max_font_size = 40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/cloud.jpg')
    print("❤❤❤❤❤❤❤❤❤❤整个网站最热门的话题前十已生成词云❤❤❤❤❤❤❤❤❤❤")

    # 将这些信息保存到本地的csv文件中
    f = open("每个讨论区最热的话题前十.csv",mode='w',encoding='utf-8-sig',newline="")
    csv_write = csv.writer(f)
    csv_write.writerow(['讨论区名称','话题名称'])
    try:
        for i in range(len(names)):
            for j in range(len(topics_total[i])):
                csv_write.writerow([names[i],topics_total[i][j]])
    except Exception as e:
        print(e)
    f.close()
    print("❤❤❤❤❤❤❤❤❤❤每个讨论区最热的话题前十已经保存到本地csv文件❤❤❤❤❤❤❤❤❤❤")


# function 2.1————find scores and speeches in some forum
def get_scores_and_speeches():
    # 将"闽越畅怀·福建"、"京华烟云"、"上海滩"、"南粤风情·广东"、"通信技术"、"Python的自由空间"、"人工智能"等几个模块链接放到列表
    urls = [
        'https://www.newsmth.net/nForum/board/Fujian?ajax',
        'https://www.newsmth.net/nForum/board/BeijingCulture?ajax',
        'https://www.newsmth.net/nForum/board/Shanghai?ajax',
        'https://www.newsmth.net/nForum/board/Guangdong?ajax',
        'https://www.newsmth.net/nForum/board/CommunTech?ajax',
        'https://www.newsmth.net/nForum/board/Python?ajax',
        'https://www.newsmth.net/nForum/board/AI?ajax'
    ]
    # 存放分数和总贴量的列表
    scores = []
    themes = []
    for url in urls:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 提取版面积分
        scores.append(int(select.xpath('//section[@id="body"]/div[2]/span[2]/text()[2]').get().split('版面积分:')[-1]))
        # 提取主题数
        themes.append(int(select.xpath('//section[@id="body"]/div[1]/div[1]/ul/li[1]/i/text()').get()))
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    names = ["闽越畅怀·福建","京华烟云","上海滩","南粤风情·广东","通信技术","Python的自由空间","人工智能"]
    plt.barh(names, themes)  # 横放条形图函数 barh
    plt.xlabel("贴数")
    plt.title('各个版块的总贴数柱状图')
    plt.savefig("pictures/各个版块的总贴数柱状图.png")
    plt.show()
    plt.barh(names, scores)  # 横放条形图函数 barh
    plt.xlabel("得分")
    plt.title('各个版块的总得分柱状图')
    plt.savefig("pictures/各个版块的总得分柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤几个版块的总得分和总贴数柱状图已绘制❤❤❤❤❤❤❤❤❤❤")



# function 2.1————Multithreading
def thread_it(func):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


# function 2.3————Add about to show information
def about():
    messagebox.showinfo('提示', '本应用用于爬取水木社区信息')


def get_fujian_topics():
    url = 'https://www.newsmth.net/nForum/board/Fujian?ajax'
    my_dict = {
        'topic': [],
        'nums': []
    }
    for i in range(1, 11):
        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
        url_end = url + '&p={}'.format(i)
        response = requests.get(url_end)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
        for info in info_range:
            reply_time = info.xpath('./td[8]/a/text()').get()
            # 筛选出是2021年的,注意是字符串
            if reply_time.split('-')[0] == '2021':
                # 筛选出话题名称和回复数
                topic = info.xpath('./td[2]/a/text()').get()
                reply_nums = info.xpath('./td[7]/text()').get()
                my_dict['topic'].append(topic)
                my_dict['nums'].append(int(reply_nums))
    topics = list(my_dict['topic'])
    scores = list(my_dict['nums'])
    limit_score = sorted(scores,reverse=True)[9]
    topic = []
    score = []
    for i in range(len(scores)):
        if scores[i] >= limit_score:
            topic.append(topics[i])
            score.append(scores[i])
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches
    plt.barh(topic, score)
    plt.xlabel("话题")
    plt.title('闽越畅怀·福建 热门话题柱状图')
    plt.savefig("pictures/闽越畅怀·福建 热门话题柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤闽越畅怀·福建 热门话题柱状图已绘制❤❤❤❤❤❤❤❤❤❤")
    # 开始绘制词云图
    words = "".join(topics).replace("转载", "").replace("完结", "").replace("Re", "").replace("已完本", "").replace("暗夜将至","")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/闽越畅怀·福建热门话题词云图.jpg')
    print("❤❤❤❤❤❤❤❤❤❤闽越畅怀·福建 热门话题词云图已绘制❤❤❤❤❤❤❤❤❤❤")


def get_beijing_topics():
    url = 'https://www.newsmth.net/nForum/board/BeijingCulture?ajax'
    my_dict = {
        'topic': [],
        'nums': []
    }
    for i in range(1, 11):
        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
        url_end = url + '&p={}'.format(i)
        response = requests.get(url_end)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
        for info in info_range:
            reply_time = info.xpath('./td[8]/a/text()').get()
            # 筛选出是2021年的,注意是字符串
            if reply_time.split('-')[0] == '2021':
                # 筛选出话题名称和回复数
                topic = info.xpath('./td[2]/a/text()').get()
                reply_nums = info.xpath('./td[7]/text()').get()
                my_dict['topic'].append(topic)
                my_dict['nums'].append(int(reply_nums))
    topics = list(my_dict['topic'])
    scores = list(my_dict['nums'])
    limit_score = sorted(scores,reverse=True)[9]
    topic = []
    score = []
    for i in range(len(scores)):
        if scores[i] >= limit_score:
            topic.append(topics[i])
            score.append(scores[i])
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches
    plt.barh(topic, score)
    plt.xlabel("话题")
    plt.title('京华烟云 热门话题柱状图')
    plt.savefig("pictures/京华烟云 热门话题柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤京华烟云 热门话题柱状图已绘制❤❤❤❤❤❤❤❤❤❤")
    # 开始绘制词云图
    words = "".join(topics).replace("转载", "").replace("完结", "").replace("Re", "").replace("已完本", "").replace("暗夜将至", "")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/京华烟云热门话题词云图.jpg')
    print("❤❤❤❤❤❤❤❤❤❤京华烟云 热门话题词云图已绘制❤❤❤❤❤❤❤❤❤❤")


def get_shanghai_topics():
    url = 'https://www.newsmth.net/nForum/board/Shanghai?ajax'
    my_dict = {
        'topic': [],
        'nums': []
    }
    for i in range(1, 11):
        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
        url_end = url + '&p={}'.format(i)
        response = requests.get(url_end)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
        for info in info_range:
            reply_time = info.xpath('./td[8]/a/text()').get()
            # 筛选出是2021年的,注意是字符串
            if reply_time.split('-')[0] == '2021':
                # 筛选出话题名称和回复数
                topic = info.xpath('./td[2]/a/text()').get()
                reply_nums = info.xpath('./td[7]/text()').get()
                my_dict['topic'].append(topic)
                my_dict['nums'].append(int(reply_nums))
    topics = list(my_dict['topic'])
    scores = list(my_dict['nums'])
    limit_score = sorted(scores,reverse=True)[9]
    topic = []
    score = []
    for i in range(len(scores)):
        if scores[i] >= limit_score:
            topic.append(topics[i])
            score.append(scores[i])
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches
    plt.barh(topic, score)
    plt.xlabel("话题")
    plt.title('上海滩 热门话题柱状图')
    plt.savefig("pictures/上海滩 热门话题柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤上海滩 热门话题柱状图已绘制❤❤❤❤❤❤❤❤❤❤")
    # 开始绘制词云图
    words = "".join(topics).replace("转载", "").replace("完结", "").replace("Re", "").replace("已完本", "").replace("暗夜将至", "")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/上海滩热门话题词云图.jpg')
    print("❤❤❤❤❤❤❤❤❤❤上海滩 热门话题词云图已绘制❤❤❤❤❤❤❤❤❤❤")


def get_guangzhou_topics():
    url = 'https://www.newsmth.net/nForum/board/Guangdong?ajax'
    my_dict = {
        'topic': [],
        'nums': []
    }
    for i in range(1, 11):
        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
        url_end = url + '&p={}'.format(i)
        response = requests.get(url_end)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
        for info in info_range:
            reply_time = info.xpath('./td[8]/a/text()').get()
            # 筛选出是2021年的,注意是字符串
            if reply_time.split('-')[0] == '2021':
                # 筛选出话题名称和回复数
                topic = info.xpath('./td[2]/a/text()').get()
                reply_nums = info.xpath('./td[7]/text()').get()
                my_dict['topic'].append(topic)
                my_dict['nums'].append(int(reply_nums))
    topics = list(my_dict['topic'])
    scores = list(my_dict['nums'])
    limit_score = sorted(scores,reverse=True)[9]
    topic = []
    score = []
    for i in range(len(scores)):
        if scores[i] >= limit_score:
            topic.append(topics[i])
            score.append(scores[i])
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches
    plt.barh(topic, score)
    plt.xlabel("话题")
    plt.title('魅力羊城·广州 热门话题柱状图')
    plt.savefig("pictures/魅力羊城·广州 热门话题柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤魅力羊城·广州 热门话题柱状图已绘制❤❤❤❤❤❤❤❤❤❤")
    # 开始绘制词云图
    words = "".join(topics).replace("转载", "").replace("完结", "").replace("Re", "").replace("已完本", "").replace("暗夜将至", "")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/魅力羊城·广州热门话题词云图.jpg')
    print("❤❤❤❤❤❤❤❤❤❤魅力羊城·广州 热门话题词云图已绘制❤❤❤❤❤❤❤❤❤❤")


def get_communication_topics():
    url = 'https://www.newsmth.net/nForum/board/CommunTech?ajax'
    my_dict = {
        'topic': [],
        'nums': []
    }
    for i in range(1, 11):
        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
        url_end = url + '&p={}'.format(i)
        response = requests.get(url_end)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
        for info in info_range:
            reply_time = info.xpath('./td[8]/a/text()').get()
            # 筛选出是2021年的,注意是字符串
            if reply_time.split('-')[0] == '2021':
                # 筛选出话题名称和回复数
                topic = info.xpath('./td[2]/a/text()').get()
                reply_nums = info.xpath('./td[7]/text()').get()
                my_dict['topic'].append(topic)
                my_dict['nums'].append(int(reply_nums))
    topics = list(my_dict['topic'])
    scores = list(my_dict['nums'])
    limit_score = sorted(scores,reverse=True)[9]
    topic = []
    score = []
    for i in range(len(scores)):
        if scores[i] >= limit_score:
            topic.append(topics[i])
            score.append(scores[i])
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches
    plt.barh(topic, score)
    plt.xlabel("话题")
    plt.title('通信技术 热门话题柱状图')
    plt.savefig("pictures/通信技术 热门话题柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤通信技术 热门话题柱状图已绘制❤❤❤❤❤❤❤❤❤❤")
    # 开始绘制词云图
    words = "".join(topics).replace("转载", "").replace("完结", "").replace("Re", "").replace("已完本", "").replace("暗夜将至", "")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/通信技术热门话题词云图.jpg')
    print("❤❤❤❤❤❤❤❤❤❤通信技术 热门话题词云图已绘制❤❤❤❤❤❤❤❤❤❤")


def get_python_free_sky_topics():
    url = 'https://www.newsmth.net/nForum/board/Python?ajax'
    my_dict = {
        'topic': [],
        'nums': []
    }
    for i in range(1, 11):
        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
        url_end = url + '&p={}'.format(i)
        response = requests.get(url_end)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
        for info in info_range:
            reply_time = info.xpath('./td[8]/a/text()').get()
            # 筛选出是2021年的,注意是字符串
            if reply_time.split('-')[0] == '2021':
                # 筛选出话题名称和回复数
                topic = info.xpath('./td[2]/a/text()').get()
                reply_nums = info.xpath('./td[7]/text()').get()
                my_dict['topic'].append(topic)
                my_dict['nums'].append(int(reply_nums))
    topics = list(my_dict['topic'])
    scores = list(my_dict['nums'])
    limit_score = sorted(scores,reverse=True)[9]
    topic = []
    score = []
    for i in range(len(scores)):
        if scores[i] >= limit_score:
            # print("❤❤❤❤❤❤❤❤❤❤闽越畅怀·福建 最热门话题是：{}❤❤❤❤❤❤❤❤❤❤".format(topics[i]))
            topic.append(topics[i])
            score.append(scores[i])
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches
    plt.barh(topic, score)
    plt.xlabel("话题")
    plt.title('Python的自由空间 热门话题柱状图')
    plt.savefig("pictures/Python的自由空间 热门话题柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤Python的自由空间 热门话题柱状图已绘制❤❤❤❤❤❤❤❤❤❤")
    # 开始绘制词云图
    words = "".join(topics).replace("转载", "").replace("完结", "").replace("Re", "").replace("已完本", "").replace("暗夜将至", "")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/Python的自由空间热门话题词云图.jpg')
    print("❤❤❤❤❤❤❤❤❤❤Python的自由空间 热门话题词云图已绘制❤❤❤❤❤❤❤❤❤❤")


def get_intelligence_topics():
    url = 'https://www.newsmth.net/nForum/board/AI?ajax'
    my_dict = {
        'topic': [],
        'nums': []
    }
    for i in range(1, 11):
        # 发现除了置顶的那些，帖子是按照最新回复的时间降序排列的，因此最多需要遍历10页就可以了
        url_end = url + '&p={}'.format(i)
        response = requests.get(url_end)
        response.encoding = response.apparent_encoding
        select = parsel.Selector(response.text)
        # 根据最后时间选择性的将对应的话题名称以及回复数添加到字典中
        info_range = select.xpath('//section[@id="body"]/div[3]/table/tbody/tr')
        for info in info_range:
            reply_time = info.xpath('./td[8]/a/text()').get()
            # 筛选出是2021年的,注意是字符串
            if reply_time.split('-')[0] == '2021':
                # 筛选出话题名称和回复数
                topic = info.xpath('./td[2]/a/text()').get()
                reply_nums = info.xpath('./td[7]/text()').get()
                my_dict['topic'].append(topic)
                my_dict['nums'].append(int(reply_nums))
    topics = list(my_dict['topic'])
    scores = list(my_dict['nums'])
    limit_score = sorted(scores,reverse=True)[9]
    topic = []
    score = []
    for i in range(len(scores)):
        if scores[i] >= limit_score:
            topic.append(topics[i])
            score.append(scores[i])
    # 绘制总体的柱状图
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches
    plt.barh(topic, score)
    plt.xlabel("话题")
    plt.title('掌上智能 热门话题柱状图')
    plt.savefig("pictures/掌上智能 热门话题柱状图.png")
    plt.show()
    print("❤❤❤❤❤❤❤❤❤❤掌上智能 热门话题柱状图已绘制❤❤❤❤❤❤❤❤❤❤")
    # 开始绘制词云图
    words = "".join(topics).replace("转载", "").replace("完结", "").replace("Re", "").replace("已完本", "").replace("暗夜将至", "")
    cut_text = "".join(jieba.cut(words))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    wCloud.to_file('pictures/掌上智能热门话题词云图.jpg')
    print("❤❤❤❤❤❤❤❤❤❤掌上智能 热门话题词云图已绘制❤❤❤❤❤❤❤❤❤❤")


if __name__ == '__main__':
    # 创建目录，保存图片
    path = 'pictures'
    # 不存在则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    top = tkinter.Tk()
    top.title('论坛舆论')
    width = 300
    height = 360
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = top.winfo_screenwidth()
    screenheight = top.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    top.geometry(alignstr)
    top.resizable(0, 0)
    # 添加button控件
    button1 = tkinter.Button(top, text="1、全站话题top10词云", width="30", command=lambda: thread_it(draw_wordcloud))
    button1.pack()
    button2 = tkinter.Button(top, text='2、讨论区话题前十', width='30', command=lambda: thread_it(draw_wordcloud))
    button2.pack()
    button3 = tkinter.Button(top, text='3、各版块总贴数和积分柱状图', width='30', command=lambda: thread_it(get_scores_and_speeches))
    button3.pack()
    button4 = tkinter.Button(top, text='4、闽越畅怀·福建top1话题', width='30', command=lambda: thread_it(get_fujian_topics))
    button4.pack()
    button5 = tkinter.Button(top, text='5、京华烟云top1话题', width='30', command=lambda: thread_it(get_beijing_topics))
    button5.pack()
    button6 = tkinter.Button(top, text='6、上海滩top1话题', width='30', command=lambda: thread_it(get_shanghai_topics))
    button6.pack()
    button7 = tkinter.Button(top, text='7、魅力羊城·广州top1话题', width='30', command=lambda: thread_it(get_guangzhou_topics))
    button7.pack()
    button8 = tkinter.Button(top, text='8、通信技术top1话题', width='30', command=lambda: thread_it(get_communication_topics))
    button8.pack()
    button9 = tkinter.Button(top, text='9、Python的自由空间top1话题', width='30', command=lambda: thread_it(get_python_free_sky_topics))
    button9.pack()
    button10 = tkinter.Button(top, text='10、掌上智能top1话题', width='30', command=lambda: thread_it(get_intelligence_topics))
    button10.pack()
    button11 = tkinter.Button(top, text='11、退出', width='30', command=top.quit)
    button11.pack()
    menu1 = tkinter.Menu(top)
    menu1.add_command(label="About", command=about)
    top.config(menu=menu1)
    # 设置窗口图标
    top.iconbitmap('logo.ico')
    top.mainloop()