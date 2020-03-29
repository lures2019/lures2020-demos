"""
    用户输入：查询的艺人
    就将该艺人所有在千千音乐的无版权歌曲下载，保存到以艺人为名的文件夹内
    将爬取到的信息保存到MongoDB数据库中！
"""
import requests
import parsel
import re
import os
import time
import pymongo
from tkinter import *
from tkinter import messagebox

headers = {
        'Cookie': 'BAIDUID=C150724507AB967B04489710A48BC855:FG=1; tracesrc=-1%7C%7C-1; u_lo=0; u_id=; u_t=; log_sid=1585485285587C150724507AB967B04489710A48BC855; Hm_lvt_d0ad46e4afeacf34cd12de4c9b553aa6=1585479174,1585485286; __qianqian_pop_tt=7; Hm_lpvt_d0ad46e4afeacf34cd12de4c9b553aa6=1585485318',
        'Host': 'music.taihe.com',
        'Referer': 'http://music.taihe.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
def get_cookie(url):
    # 原始网页的URL
    url = url
    s = requests.Session()
    s.get(url, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    return cookie

def download_music(kd,page):
    # key=后面的是【艺人】名称的Unicode编码
    kd = kd
    word = str(bytes(kd, encoding="utf-8")).replace(r"b'", '').replace("'", '').replace(r"\x", "%").upper()
    url = 'http://music.taihe.com/search?key={}'.format(word)
    params = {
        'key': kd,
        'start': str(20*page),
        'size': '20'
    }
    response = requests.get(url=url, headers=headers, params=params,cookies=get_cookie(url))
    response.encoding = response.apparent_encoding
    select = parsel.Selector(response.text)
    song_ids = select.xpath('//div[@class="song-item clearfix "]/span[@class="song-title"]/a/@href').getall()
    # http://music.taihe.com/song/242078437
    path = kd
    if not os.path.exists(path):
        os.mkdir(path)
    # 连接MongoDB
    client = pymongo.MongoClient(host='localhost', port=27017)
    # 指定数据库
    db = client.qianqian_music
    collection = db.music_message
    try:
        for song_id in song_ids:
            song_id = re.findall('\d+', song_id)
            if len(song_id) != 0:
                data = {}
                url = 'http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&songid={}&from=web'.format(
                    song_id[0])
                response = requests.get(url=url)
                response.encoding = response.apparent_encoding
                html = response.json()
                data['歌曲名'] = html['songinfo']['title']  # 歌曲名
                data['歌曲链接'] = html['bitrate']['show_link']  # 歌曲链接
                data['收藏数'] = html['songinfo']['collect_num']  # 收藏数
                data['千千音乐播放量'] = html['songinfo']['hot']  # 千千音乐播放量
                data['总播放量'] = html['songinfo']['total_listen_nums']  # 总播放量
                data['发行时间'] = html['songinfo']['publishtime']  # 发行时间
                new_url = html['bitrate']['show_link']
                new_response = requests.get(url=new_url)
                with open(path + '/' + html['songinfo']['title'] + '.mp3', mode="wb") as f:
                    f.write(new_response.content)
                collection.insert(data)
                print(html['songinfo']['title'] + '>>>>>>>>下载完毕！且数据保存到MongoDB！<<<<<<<<')
    except Exception as error:
        print("该歌曲存在版权保护，无法下载！")


def get_url():
    kd = entry.get()
    kd = kd.strip()
    if kd == "":
        messagebox.showinfo("提示", "请输入有效的艺人姓名！")
    else:
        try:
            word = str(bytes(kd, encoding="utf-8")).replace(r"b'", '').replace("'", '').replace(r"\x", "%").upper()
            url = 'http://music.taihe.com/search?key=' + word
            response = requests.get(url=url, headers=headers, cookies=get_cookie(url))
            select = parsel.Selector(response.text)
            pages = select.xpath(
                '//div[@id="result_container"]/div[1]/div[2]/div/div/a[@class="page-navigator-number 		PNNW-S"]/text()').getall()[
                -1]
            for page in range(int(pages)):
                download_music(kd, page)
                result.set("第{}页数据采集完毕！".format(page + 1))
                time.sleep(2)
        except Exception as error:
            messagebox.showinfo("警告", "没有该艺人的信息！")




window = Tk()
window.geometry("380x100+600+400")
window.resizable(0, 0)
window.title("千千音乐V2.0")

# 控件
label = Label(window, text="请输入您想查询的艺人姓名：", font=("仿宋", 12))
label.grid(row=0, column=0, sticky=W)
entry = Entry(window, font=("仿宋", 12))
entry.grid(row=0, column=1)

label1 = Label(window, text="当前数据情况：", font=("仿宋", 12))
label1.grid(row=1, column=0, sticky=W)
result = StringVar()
entry1 = Entry(window, font=("仿宋", 12),textvariable=result)
entry1.grid(row=1, column=1)

label2 = Label(window,text="")
label2.grid(row=2, column=0)

# 按钮
button = Button(window, text="开始爬取", font=("仿宋", 12), width="12", command=get_url)
button.grid(row=3, column=0, sticky=W)
button1 = Button(window, text="退出", font=("仿宋", 12), width="10",command=window.quit)
button1.grid(row=3, column=1, sticky=E)

window.mainloop()