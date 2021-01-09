"""
    (1)爬取搜索词为"思政课"100个左右视频的评论
    (2)爬取搜索词为"文化自信"100个左右视频的评论
"""
import requests
import threading
import parsel
import re
import os
import csv


# 2、开多线程
def thread_it(func):
    """将函数打包进线程"""
    # 创建
    t = threading.Thread(target=func)
    # 守护
    t.setDaemon(True)
    # 启动
    t.start()


# 1、爬取"思政课"100个左右视频的评论
class function1(object):
    def __init__(self,url,path):
        self.url = url
        self.path = path

    # 100个思政视频的详细统计信息
    def save_all_videos_information_to_csv(self):
        response = requests.get(self.url)
        # 设置万能解码
        response.encoding = response.apparent_encoding
        # 一页20个视频，需要爬5页
        select = parsel.Selector(response.text)
        # 视频标题
        titles = select.xpath('//ul[@class="video-list clearfix"]/li/a/@title').getall()
        # 视频链接
        urls = select.xpath('//ul[@class="video-list clearfix"]/li/a/@href').getall()
        # 转换为真正的视频链接
        real_urls = ['https:' + i for i in urls]
        # https://www.bilibili.com/video/BV1S4411a7xP?from=search&seid=3998064449059550761
        """下面的部分，需要对个体进行字符串的处理"""
        # 视频时长
        time = select.xpath('//ul[@class="video-list clearfix"]/li/a/div[@class="img"]/span/text()').getall()
        # 观看人数
        persons = select.xpath('//ul[@class="video-list clearfix"]/li/div[@class="info"]/div[@class="tags"]/span[1]/text()').getall()
        # 弹幕数
        barrages = select.xpath('//ul[@class="video-list clearfix"]/li/div[@class="info"]/div[@class="tags"]/span[2]/text()').getall()
        # 上传时间
        update_times = select.xpath('//ul[@class="video-list clearfix"]/li/div[@class="info"]/div[@class="tags"]/span[3]/text()').getall()
        # up主昵称
        up_names = select.xpath('//ul[@class="video-list clearfix"]/li/div[@class="info"]/div[@class="tags"]/span[4]/a/text()').getall()

        # 创建csv文件，因为需要仅第一行是有标头的，因此需要根据url最后的page是否为1进行判断
        page = int(self.url.split("&page=")[-1])
        if page == 1:
            f = open(self.path + '/' + "100个视频详细信息.csv",newline="",mode="w",encoding="utf-8-sig")
            csv_write = csv.writer(f)
            csv_write.writerow(["视频标题","视频时长","观看人数","弹幕数","up主昵称","上传时间","视频链接"])
            # 下面开始遍历
            for i in range(len(titles)):
                person_now = persons[i].replace("\n","").strip()
                barrage_now = barrages[i].replace("\n","").strip()
                update_time_now = update_times[i].replace("\n","").strip()
                up_name_now = up_names[i].replace("\n","").strip()
                # 开始按行写入csv文件
                csv_write.writerow([titles[i],time[i],person_now,barrage_now,up_name_now,update_time_now,real_urls[i]])
            f.close()
        else:
            f = open(self.path + '/' + "100个视频详细信息.csv", newline="", mode="a+", encoding="utf-8-sig")
            csv_write = csv.writer(f)
            # 下面开始遍历
            for i in range(len(titles)):
                person_now = persons[i].replace("\n", "").strip()
                barrage_now = barrages[i].replace("\n", "").strip()
                update_time_now = update_times[i].replace("\n", "").strip()
                up_name_now = up_names[i].replace("\n", "").strip()
                # 开始按行写入csv文件
                csv_write.writerow([titles[i], time[i], person_now, barrage_now, up_name_now, update_time_now, real_urls[i]])
        print("100个视频详细信息统计已完成{}/5".format(page))

    # 100个视频的评论链接
    def get_comments_link(self):
        url = self.url
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        # 使用正则表达式提取av号码,匹配后返回是一个列表
        try:
            av_number = re.findall('<meta data-vue-meta="true" itemprop="url" content="https://www.bilibili.com/video/av(.*?)/">',response.text)[0]
            # 下面是评论的链接,pn后面是页数，默认1页，但有些很明显超过此页数
            comment_url = 'https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid={}&sort=1'.format(av_number)
            # 返回评论链接
            return comment_url
        except Exception as error:
            print(error)

    # 解析评论
    def analyse_comments(self):
        url = self.url
        path = self.path
        response = requests.get(url)
        # 只能设置为utf-8，否则直接乱码
        response.encoding = 'utf-8'
        # 使用json提取到 回复
        try:
            datas = response.json()['data']['replies']
            # 打开文件，追加内容
            f = open(path + '/' + "100个视频评论信息.csv",mode="a+",newline="",encoding="utf-8-sig")
            csv_write = csv.writer(f)
            for data in datas:
                # 回复内容
                message = data['content']['message']
                # 回复id
                id = data['member']['mid']
                # 昵称
                uname = data['member']['uname']
                # 性别
                sex = data['member']['sex']
                csv_write.writerow([message,id,uname,sex])
            f.close()
        # 遇到报错信息就打印出来
        except Exception as error:
            print("该视频无评论！")


# 2、思政课主函数调用代码折叠
def political():
    path = "思政课"
    # 如果不存在此文件夹则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(1,6):
        url = 'https://search.bilibili.com/all?keyword=%E6%80%9D%E6%94%BF%E8%AF%BE&from_source=nav_search_new&page={}'.format(i)
        start = function1(url,path)
        start.save_all_videos_information_to_csv()
    """以上部分完成了100个思政视频详细信息的统计，根据此我们爬取每个视频的评论"""
    # 首先读取上面的csv文件，获取所有网址集合
    f = open(path + '/' +'100个视频详细信息.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 获取链接
    urls = [row[-1] for row in rows[1:]]
    # https://www.bilibili.com/video/BV1S4411a7xP?from=search
    # 获取评论链接
    comments_urls = []
    # 下面可以考虑调用函数了
    for url in urls:
        start = function1(url,path)
        # 此处加不了多线程，/(ㄒoㄒ)/~~
        comments_urls.append(start.get_comments_link())
    # 开始将评论链接写入原csv文件中
    fp = open(path + '/' +"100个视频详细信息.csv",mode="w",newline="",encoding='utf-8-sig')
    csv_write = csv.writer(fp)
    rows[0].append("评论链接")
    csv_write.writerow(rows[0])
    for i in range(1,len(rows)):
        rows[i].append(comments_urls[i-1])
        csv_write.writerow(rows[i])
    fp.close()
    # 下面开始爬取评论,考虑用多线程
    # 开始创建csv文件
    f_now = open(path +'/' + '100个视频评论信息.csv',mode='w',encoding='utf-8-sig',newline="")
    csv_write_now = csv.writer(f_now)
    csv_write_now.writerow(['B站id','昵称','性别','回复内容'])
    f_now.close()
    for url in comments_urls:
        start = function1(url,path)
        thread_it(start.analyse_comments())

# 3、文化自信可以和思政共用一套体系
def culture_confidence():
    path = "文化自信"
    # 如果不存在此文件夹则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(1,6):
        url = 'https://search.bilibili.com/all?keyword=%E6%96%87%E5%8C%96%E8%87%AA%E4%BF%A1&from_source=nav_search_new&page={}'.format(i)
        start = function1(url,path)
        start.save_all_videos_information_to_csv()
    """以上部分完成了100个思政视频详细信息的统计，根据此我们爬取每个视频的评论"""
    # 首先读取上面的csv文件，获取所有网址集合
    f = open(path + '/' +'100个视频详细信息.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 获取链接
    urls = [row[-1] for row in rows[1:]]
    # https://www.bilibili.com/video/BV1S4411a7xP?from=search
    # 获取评论链接
    comments_urls = []
    # 下面可以考虑调用函数了
    for url in urls:
        start = function1(url,path)
        # 此处加不了多线程，/(ㄒoㄒ)/~~
        comments_urls.append(start.get_comments_link())
    # 开始将评论链接写入原csv文件中
    fp = open(path + '/' +"100个视频详细信息.csv",mode="w",newline="",encoding='utf-8-sig')
    csv_write = csv.writer(fp)
    rows[0].append("评论链接")
    csv_write.writerow(rows[0])
    for i in range(1,len(rows)):
        rows[i].append(comments_urls[i-1])
        csv_write.writerow(rows[i])
    fp.close()
    # 下面开始爬取评论,考虑用多线程
    # 开始创建csv文件
    f_now = open(path +'/' + '100个视频评论信息.csv',mode='w',encoding='utf-8-sig',newline="")
    csv_write_now = csv.writer(f_now)
    csv_write_now.writerow(['B站id','昵称','性别','回复内容'])
    f_now.close()
    for url in comments_urls:
        try:
            start = function1(url,path)
            thread_it(start.analyse_comments())
        except Exception as error:
            print(error)


# 4、中国医学史可以共用一个体系
def medicine_history():
    path = "中国医学史"
    # 如果不存在此文件夹则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(1,3):
        url = 'https://search.bilibili.com/all?keyword=%E4%B8%AD%E5%9B%BD%E5%8C%BB%E5%AD%A6%E5%8F%B2&from_source=nav_search_new&page={}'.format(i)
        start = function1(url,path)
        start.save_all_videos_information_to_csv()
    """以上部分完成了100个思政视频详细信息的统计，根据此我们爬取每个视频的评论"""
    # 首先读取上面的csv文件，获取所有网址集合
    f = open(path + '/' +'100个视频详细信息.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 获取链接
    urls = [row[-1] for row in rows[1:]]
    # https://www.bilibili.com/video/BV1S4411a7xP?from=search
    # 获取评论链接
    comments_urls = []
    # 下面可以考虑调用函数了
    for url in urls:
        start = function1(url,path)
        # 此处加不了多线程，/(ㄒoㄒ)/~~
        comments_urls.append(start.get_comments_link())
    # 开始将评论链接写入原csv文件中
    fp = open(path + '/' +"100个视频详细信息.csv",mode="w",newline="",encoding='utf-8-sig')
    csv_write = csv.writer(fp)
    rows[0].append("评论链接")
    csv_write.writerow(rows[0])
    for i in range(1,len(rows)):
        rows[i].append(comments_urls[i-1])
        csv_write.writerow(rows[i])
    fp.close()
    # 下面开始爬取评论,考虑用多线程
    # 开始创建csv文件
    f_now = open(path +'/' + '100个视频评论信息.csv',mode='w',encoding='utf-8-sig',newline="")
    csv_write_now = csv.writer(f_now)
    csv_write_now.writerow(['B站id','昵称','性别','回复内容'])
    f_now.close()
    for url in comments_urls:
        try:
            start = function1(url,path)
            thread_it(start.analyse_comments())
        except Exception as error:
            print(error)



if __name__ == '__main__':
    # 以下三个函数分别对应任务1，2，4
    political()
    culture_confidence()
    medicine_history()