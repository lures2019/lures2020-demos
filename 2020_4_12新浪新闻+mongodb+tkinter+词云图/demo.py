"""
    需求：
        通过对爬虫技术的分析与研究，设计基于Python的网络聚焦爬虫，实现对新闻网站的爬取以及可视化管理配置。
        研究主流的分布式爬虫技术，根据各项需求进行系统功能的总体设计、详细设计以及程序设计与测试。
        系统采用图形化界面，对新闻进行分析和可视化。使用户更简单方便的查看产品的信息。
"""
# -*- coding:utf-8 -*-
import tkinter
import requests
import time
import pymongo
import jieba
import cv2
from wordcloud import WordCloud, STOPWORDS
from string import digits

top = tkinter.Tk()
top.title('新闻News')
top.geometry('500x300')
top.resizable(0,0)

def request_get(url, headers=None):
    # HTTP请求
    response_get = requests.get(url, headers=headers)
    response_get.encoding = response_get.apparent_encoding
    if response_get.status_code == 200:
        return response_get.text
    return '请求失败！', response_get.status_code

def main():
    f = open("统计词.txt",encoding="utf-8",mode="w")
    headers = {
        'cookie': 'SUB=_2AkMp0vSTf8NxqwJRmf0Rym_qaIhxyA7EieKfjgVIJRMyHRl-yD9jqnQEtRB6AlLafEyryczOfN-C0GOE0Y-GhPGXQHup; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WW2fc8oz.Q78QUBffxKeZ.6; UOR=cn.bing.com,www.sina.com.cn,; SGUID=1586685950615_19517350; SINAGLOBAL=124.128.144.101_1586685952.270239; Apache=124.128.144.101_1586685952.270241; UM_distinctid=1716dda465087-0ff5dc081deccc-376b4502-ff000-1716dda4651733; BAIDU_SSP_lcr=https://cn.bing.com/; lxlrttp=1578733570; ULV=1586686307338:2:2:2:124.128.144.101_1586685952.270241:1586685951474; FEED-MIX-SINA-COM-CN=',
        'referer': 'https://news.sina.com.cn/china/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    titles = []  # 新闻标题
    urls = []  # 新闻链接
    # 连接MongoDB
    client = pymongo.MongoClient(host='localhost', port=27017)
    # 指定数据库
    db = client.news
    collection = db.news_message
    for i in range(1,10):
        params = {
            'pageid': '121',
            'lid': '1356',
            'num': '20',
            'versionNumber': '1.2.4',
            'page': str(i)
        }
        url = 'https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page=' + str(i)
        try:
            while True:
                html = request_get(url, headers)
                tt.delete(1.0, tkinter.END)
                response = requests.get(url=url, headers=headers, params=params)
                response.encoding = 'utf-8'
                results = response.json()['result']['data']
                for result in results:
                    data = {}
                    titles.append(result['title'])
                    data['标题'] = result['title']
                    urls.append(result['url'])
                    data['链接'] = result['url']
                    collection.insert(data)
                    remove_digits = str.maketrans('', '', digits)
                    res = result['title'].translate(remove_digits)
                    f.write(res)
                break
        except requests.exceptions.ConnectionError:
            tt.insert('end', '网络报错！正在重新获取信息。。。请短时间内搞定网络，否则程序中断。\n')
            tt.update()
            time.sleep(2)
            main()
    for t, u in zip(titles, urls):
        tt.insert('end', '-' * 70 + '\n')
        tt.insert('end', '{}\n{}\n'.format(t, u))
    f.close()
    with open('统计词.txt', 'r',encoding='utf-8') as f:
        text = f.read()
    cut_text = " ".join(jieba.cut(text))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # font_path=path.join(d,'simsun.ttc'),
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=2000,
        # 最大号字体
        max_font_size=40
    )

    wCloud = cloud.generate(cut_text)
    wCloud.to_file('cloud.jpg')
button1 = tkinter.Button(top, text='运行',width="10",command=main).grid(row=0,column=0,sticky='w')
button2 = tkinter.Button(top,text="退出",width="10",command=top.quit).grid(row=0,column=0)
tt = tkinter.Text(top, height=33,width="130")
tt.grid()


top.mainloop()
