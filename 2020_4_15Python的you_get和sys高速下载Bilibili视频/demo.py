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
    url = 'https://www.bilibili.com/video/BV1Np4y1Q7mB?from=search&seid=612506582011803639'
    path = 'video'
    if not os.path.exists(path):
        os.mkdir(path)
    download_video(path,url)

ExtracVideo()
