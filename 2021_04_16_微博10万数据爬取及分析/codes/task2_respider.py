import requests
import datetime
import re
import csv
from pymongo import MongoClient
from multiprocessing import Pool
import time
from fake_useragent import UserAgent



def main(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    datas = response.json()['data']['data']
    # 追写csv文件
    f = open('新疆棉事件转发用户信息.csv', mode='a+', encoding='utf-8-sig', newline='')
    csv_write = csv.writer(f)
    # 链接MongoDB数据库
    client = MongoClient()
    collection = client["XinJiang_cotton"]["XinJiang_cotton"]
    # 构造月份字典
    months = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    # 针对 用户的性别和年龄信息的爬虫 反爬设置
    ua = UserAgent()
    # https://cloud.tencent.com/developer/article/1636419
    headers = {
        'user-agent': ua.random,
        'cookie': '_T_WM=51964647749; SCF=Ag_QCRA7R5GGlw8lnbADIcPAen3LZMuxqjLzz8utGAi7SHq4WFsOWBfo7ReMY7BKw3sgJO7NNwhXmk2o9gzNRMk.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF5lTJn4o6Q1SkwywcTGfHs5JpX5KMhUgL.FoMpSo.XehMceon2dJLoI7DjUPiLMfS_IPxQ; M_WEIBOCN_PARAMS=oid%3D4626586583697376%26luicode%3D10000011%26lfid%3D231522type%253D61%2526q%253D%2523%25E6%2596%25B0%25E7%2596%2586%25E6%25A3%2589%2523%2526t%253D10; SUB=_2A25NfcGODeRhGeFP7VsV8CnKyTSIHXVuge_GrDV6PUJbkdAKLUfbkW1NQRvkfURdxNIzXa56AtZEyQfa0hjLWdo4; SSOLoginState=1618588126; WEIBOCN_FROM=1110106030; MLOGIN=1'
    }
    for data in datas:
        try:
            # 得到的时间数据类似这种：['Fri', 'Apr', '16', '22:12:17', '+0800', '2021']
            pub_time = data['created_at'].split()
            # 构造正确的时间形式
            right_time = pub_time[-1] + '-' + months[pub_time[1]] + '-' + pub_time[2] + ' ' + pub_time[3]
            # 转换为datatime类型
            date_time = datetime.datetime.strptime(right_time, '%Y-%m-%d %H:%M:%S')

            # 提取 发布信息平台
            source = data['source']
            # 提取 用户的id
            id = data['user']['id']
            # 提取 用户的昵称
            name = data['user']['screen_name']
            # 提取 用户的性别,f和m分别代表女生/男生
            gender = data['user']['gender']

            """更换接口：爬取年龄和地区信息"""
            url1 = 'https://weibo.cn/{}/info'.format(id)
            response1 = requests.get(url1, headers=headers)
            response1.encoding = response1.apparent_encoding
            # 构造正则表达式进行提取
            # <br/>地区:陕西 西安<br/>生日:1993-11-19<br/>
            area = re.findall("<br/>地区:(.*?)<br/>", response1.text)
            birth = re.findall("<br/>生日:(.*?)<br/>", response1.text)
            # 有些用户不写生日和地区信息，重新处理
            area = ["" if area == [] else area[0]]
            birth = ["" if birth == [] else birth[0]]
            csv_write.writerow([date_time, area[0], source, name, gender, birth[0]])
            # 构造MongoDB数据库存储形式
            item = {
                '转发时间': right_time,
                '所在地区': area[0],
                '发布平台': source,
                '用户昵称': name,
                '性别': gender,
                '出生日期': birth[0]
            }
            # 插入到数据库中
            collection.insert_one(item)
            print(item)
        except Exception as error:
            print(error,url)
    f.close()
    # time.sleep(2)
    print("❤❤❤❤❤❤❤❤❤❤已经抓取1页信息❤❤❤❤❤❤❤❤❤❤")


if __name__ == '__main__':
    # 创建csv文件用于保存数据
    start = time.time()
    f = open('新疆棉事件转发用户信息.csv', mode='a+', encoding='utf-8-sig', newline='')
    csv_write = csv.writer(f)
    # csv_write.writerow(['转发时间', '所在地区', '发布平台', '用户昵称', '性别', '出生日期'])
    f.close()
    # 开启四进程
    pool = Pool(processes=8)
    urls = []
    # 1页10条数据，爬10000页
    try:
        for page in range(1, 10001):
            url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=4618389982546373&page={}'.format(page)
            urls.append(url)
    except Exception as error:
        print(error)
    pool.map(main, urls)
    pool.close()
    pool.join()
    end = time.time()
    print("耗时：{}秒".format(end - start))