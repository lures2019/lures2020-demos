"""
        (3)爬取搜索词为"医学史"出现的两个课程的评论{
        北大张大庆：
            https://www.bilibili.com/video/BV1Lx411j7RG?from=search&seid=7741191970619942527
        黑龙江常存库：
            https://www.bilibili.com/video/BV1x441147w1?from=search&seid=7741191970619942527
    }
"""
import requests
import os
import csv
import re

"""目测，因为就两个视频系列，可以直接得出av号"""
def get_comment_urls(url):
    url = url
    response = requests.get(url)
    # 设置万能解码
    response.encoding = response.apparent_encoding
    # 提取av后面的数字，是评论链接的一个参数，是列表形式给出的
    av_id = re.findall('<meta data-vue-meta="true" itemprop="url" content="https://www.bilibili.com/video/av(.*?)/">',response.text)[0]
    # 查看原视频可以看到评论只有2页
    # 构造评论链接列表
    comment_urls = []
    for i in range(1, 3):
        comment_url = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&sort=1'.format(i, av_id)
        comment_urls.append(comment_url)
    return comment_urls

def save_comments_to_csv(path,url):
    f = open(path + '/' + "评论信息.csv",mode="a+",encoding="utf-8-sig",newline="")
    csv_write = csv.writer(f)
    # 提取页数page
    page = int(url.split("?pn=")[-1].split('&')[0])
    # 若为1，则写上标头
    if page == 1:
        csv_write.writerow(['昵称','性别','回复内容','B站id'])
    # 获取响应信息
    response = requests.get(url)
    response.encoding = 'utf-8'
    try:
        datas = response.json()['data']['replies']
        for data in datas:
            # 回复内容
            message = data['content']['message']
            # 回复id
            id = data['member']['mid']
            # 昵称
            uname = data['member']['uname']
            # 性别
            sex = data['member']['sex']
            csv_write.writerow([message, id, uname, sex])
    except Exception as error:
        print(error)


if __name__ == '__main__':
    # 先创建一个文件夹用于存储数据
    names = ['北大张大庆','黑龙江常存库']
    for name in names:
        if not os.path.exists(name):
            os.mkdir(name)
    urls = ['https://www.bilibili.com/video/BV1Lx411j7RG?from=search&seid=7741191970619942527','https://www.bilibili.com/video/BV1x441147w1?from=search&seid=7741191970619942527']
    for i in range(len(urls)):
        # 得到评论的地址
        comment_urls = get_comment_urls(urls[i])
        # 开始调用函数解析
        for url in comment_urls:
            save_comments_to_csv(names[i],url)
        print("第{}个课程评论爬取完毕！".format(i+1))

