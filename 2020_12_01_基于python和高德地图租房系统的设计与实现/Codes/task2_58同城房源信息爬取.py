"""
    Task1：爬取深圳市龙华区在58同城上的租房信息（租房价格2000-4000）
"""
import requests
from lxml import etree
import base64
import random
from io import BytesIO
from multiprocessing import Pool
import csv
import re
from fontTools.ttLib import TTFont

# 0、读取ip
def get_proxies():

    with open('ip.txt', 'r') as f:
        result = f.readlines()  # 读取所有行并返回列表
    proxy_ip = random.choice(result)[:-1]  # 获取了所有代理IP
    L = proxy_ip.split(':')
    proxy_ip = {
        # 'http': 'http://{}:{}'.format(L[0], L[1]),
        'https': 'https://{}:{}'.format(L[0], L[1])
    }
    return proxy_ip

# 1、获取信息
def get_information(url):
    url = url
    proxies = get_proxies()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers,proxies=proxies,timeout=5)
        response.encoding = response.apparent_encoding
        # 反爬字体
        bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", response.text)[0]
        html = etree.HTML(response.text, etree.HTMLParser())
        # 开始寻找 相关有用信息变量
        # 根据xpath提取第一页只有84张照片，而网页显示99张,url.split('?')[0]获取原图
        # img_urls是图片链接集
        img_urls = html.xpath('//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="img-list"]/a/@href')
        # titles是房源标题,先title.replace('\n','').strip()去掉无用项，接着len(x) > 0就是标题,也是84个有用信息
        titles = html.xpath('//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="des"]/h2/a/text()')
        # communtiys代表小区名称，只有83个信息
        communitys = html.xpath('//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="des"]/p[@class="infor"]/a[2]/text()')
        # 房价信息
        prices = html.xpath('//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="list-li-right"]/div[@class="money"]/b/text()')

        return bs64_str,  titles, communitys, prices,img_urls
    except Exception as e:
        get_information(url)

# 2、破解字体加密
def get_page_show_ret(str1,string):
    bs64_str = str1
    font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
    c = font.getBestCmap()
    ret_list = []
    for char in string:
        decode_num = ord(char)
        if decode_num in c:
            num = c[decode_num]
            num = int(num[-2:]) - 1
            ret_list.append(num)
        else:
            ret_list.append(char)
    ret_str_show = ''
    for num in ret_list:
        ret_str_show += str(num)
    return ret_str_show

# 3、保存数据到csv文件
def save_data_to_csv(url):
    url = url
    bs64_str,  titles, communitys, prices,img_urls = get_information(url)
    # 列表长度82
    img_urls_now = [url.split('?')[0] for url in img_urls]
    # 列表长度82
    titles_now = []
    for title in titles:
        x = title.replace('\n','').strip()
        if len(x) > 0:
            titles_now.append(get_page_show_ret(bs64_str,x))
    # communitys列表长度是82,prices_now列表长度就是82
    prices_now = [get_page_show_ret(bs64_str,price) for price in prices]

    return titles_now,communitys,prices_now,img_urls_now


# 4、开启多进程
def main(url):
    f = open("深圳龙华房源信息.csv",mode='a+',encoding='utf-8-sig',newline="")
    csv_write = csv.writer(f)
    try:
        titles_now, communitys, prices_now, img_urls_now = save_data_to_csv(url)
        for i in range(min(len(titles_now), len(communitys), len(prices_now), len(img_urls_now))):
            csv_write.writerow([titles_now[i], communitys[i], prices_now[i], img_urls_now[i]])
        print("已经爬取1页！")
    except Exception as error:
        print(error,"此代理失效！")


if __name__ == '__main__':
    # 开启四进程
    pool = Pool(processes=4)
    urls = []
    for j in range(1,71):
        if (j == 1):
            url = 'https://sz.58.com/szlhxq/chuzu/?minprice=2000_4000&sourcetype=5'
            urls.append(url)
        else:
            url = 'https://sz.58.com/szlhxq/chuzu/pn{}/?minprice=2000_4000&sourcetype=5'.format(j)
            urls.append(url)
    pool.map(main, urls)
    pool.close()
    pool.join()
    print("爬取完毕！")