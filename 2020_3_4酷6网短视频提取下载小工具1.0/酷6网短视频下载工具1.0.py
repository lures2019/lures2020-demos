"""
需求：
    1)、爬取的网站地址：https://www.ku6.com/index
    2)、输出几个栏目，用户输入想要爬取的栏目名爬取相应的视频的真实url以及标题到对应文件名的csv文件中
    3)、用户输入csv文件中显示的某一视频的url地址开始下载视频并保存到"下载"目录中
    4)、显示下载所用时间
暂未实现的功能：
    1)、图形化界面GUI
    2)、显示下载进度条以及下载速度
"""
import requests
import time,csv,os

def get_url(kd):
    if kd == '首页':
        url = ''
    elif kd == '资讯':
        url = '&subjectId=69'
    elif kd == '娱乐':
        url = '&subjectId=70'
    elif kd == '短酷':
        url = '&subjectId=76'
    elif kd == '自制节目':
        url = '&subjectId=71'
    elif kd == '影视':
        url = '&subjectId=72'
    elif kd == '音乐':
        url = '&subjectId=74'
    elif kd == '原创':
        url = '&subjectId=75'
    elif kd == '生活':
        url = '&subjectId=80'
    elif kd == '游戏':
        url = '&subjectId=93'
    elif kd == '健康':
        url = '&subjectId=81'
    elif kd == '汽车':
        url = '&subjectId=47'
    elif kd == '动漫':
        url = '&subjectId=145'
    elif kd == '造就':
        url = '&subjectId=184'
    else:
        print("您输入的选项有问题，没有该栏目名！请关闭软件重新运行！")
        # 休眠10s以便于用户看到此消息
        time.sleep(10)
    save_data(url,kd)

def save_data(url,kd):
    pages = int(input('请输入想爬取的页数：(eg:10)'))
    f = open(kd + '.csv',mode="a+",newline='',encoding="utf_8_sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['视频名称','视频地址'])

    titles = [[] for i in range(pages)]
    playUrls = [[] for i in range(pages)]
    for i in range(pages):
        new_url = 'https://www.ku6.com/video/feed?pageNo={}&pageSize=40{}'.format(i,url)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'BAIDU_SSP_lcr=https://cn.bing.com/; Hm_lvt_6b95cc5cc615e00b34bb663673148c6c=1583236780,1583237949; Hm_lvt_cadc05fa9075c3aea60585cd886a188c=1583237951; Hm_lpvt_cadc05fa9075c3aea60585cd886a188c=1583247633; Hm_lpvt_6b95cc5cc615e00b34bb663673148c6c=1583247715',
            'referer': 'https://www.ku6.com/index'
        }
        response = requests.get(url=new_url,headers=headers)
        for j in range(len(response.json()['data'])):
            titles[i].append(response.json()['data'][j]['title'])
            playUrls[i].append(response.json()['data'][j]['playUrl'])
            csv_write.writerow([titles[i][j],playUrls[i][j]])
        print('——————————————第{}页爬取完毕！————————————————'.format(str(i+1)))
        csv_write.writerow(['\n','\n'])
        time.sleep(1)

def video_download(url,title):
    path = '视频'
    if not os.path.exists(path):
        os.mkdir(path)
    response = requests.get(url)
    with open(path + '/' + title + '.mp4',mode="wb") as f:
        f.write(response.content)

if __name__ == '__main__':
    print("当前导航栏共有栏目：[首页、资讯、娱乐、短酷、自制节目、影视、音乐、原创、生活、游戏、健康、汽车、动漫、造就]")
    kd = input("请输入您想爬取的栏目名：(eg:首页)")
    start_time = time.time()
    get_url(kd)
    end_time = time.time()
    print('抓取数据并保存到csv文件中总耗时：{}秒'.format(str(end_time-start_time)))
    time.sleep(2)
    url = input('请从保存的csv文件中下载您需要的视频(输入视频的地址就可以)：')
    title = input('请输入保存此视频所用的文件名称(建议使用csv文件中标题，但注意不要、之类的不规范字符)')
    start = time.time()
    video_download(url,title)
    end = time.time()
    print('该视频下载的时间是：{}秒'.format(str(end-start)))
    time.sleep(2)
