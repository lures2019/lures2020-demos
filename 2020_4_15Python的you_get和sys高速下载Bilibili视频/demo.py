# you_get可以包含对VIP视频/电影/短片/小视频的下载
import you_get
import os
import sys
import json
import requests

def download_video(path,url):
    # 调用指令，-o是指令的参数,sys操纵系统模块
    sys.argv = ['you-get','-o',path,url]
    # 默认下载是flv格式
    you_get.main()

def ExtracVideo():
    """提取网页中的视频播放地址"""
    url = 'https://s.search.bilibili.com/cate/search?callback=jqueryCallback_bili_7538234669394426&main_ver=v3&search_type=video&view_type=hot_rank&order=click©_right=-1&cate_id=25&page=1&pagesize=20&jsonp=jsonp&time_from=20200408&time_to=20200415&_=1586934006126'
    # 伪造浏览器请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }
    response = requests.get(url,headers=headers).text
    # 取数据并把数据转化为json数据格式,数据的切片
    json_data = json.loads(response[37:-1])
    data = json_data['result']
    for i in data:
        # 取到视频的播放地址
        arcurl = i['arcurl']
        path = 'video'
        if not os.path.exists(path):
            os.mkdir(path)
        download_video(path,arcurl)

ExtracVideo()