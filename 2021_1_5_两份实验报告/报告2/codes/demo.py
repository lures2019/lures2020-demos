"""
    Python实战——爬取彼岸图网的4k动漫图片！
    思路：
        1）分析4k动漫url
        2）找到每个页面的图片之间的联系
        3）提取到此页面图片的url，打开新的界面，开始分析网页，获取真实的4k图
    知识点：
        1）简单的页面分析
        2）Xpath选择器提取有用信息
"""

import requests
import parsel
import os
import time


# http://pic.netbian.com/4kdongman/index_132.html
def download_images(i,url):
    page = i
    headers = {
        'Cookie': '__cfduid=d009c33b3bbb80a4c62566e6dc10ca9781586700477; zkhanecookieclassrecord=%2C66%2C; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1588136909,1588650084,1588650428,1588651115; PHPSESSID=1k8k9g1m8gs9u0prcvs850g132; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1588658025',
        'Host': 'pic.netbian.com',
        'Referer': 'http://pic.netbian.com/4kdongman/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding  # 万能解码
    select = parsel.Selector(response.text)

    image_urls = select.xpath('//div[@id="main"]/div[@class="slist"]/ul[@class="clearfix"]/li/a/@href').getall()
    image_names = select.xpath('//div[@id="main"]/div[@class="slist"]/ul[@class="clearfix"]/li/a/b/text()').getall()

    path = "4k动漫壁纸"
    if not os.path.exists(path):
        os.mkdir(path)

    for i in range(len(image_names)):
        url = 'http://pic.netbian.com' + image_urls[i]
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        new_select = parsel.Selector(response.text)
        real_image_url = new_select.xpath('//div[@class="photo-pic"]/a[@id="img"]/img/@src').get()
        real_response = requests.get('http://pic.netbian.com' + real_image_url)
        # http://pic.netbian.com/uploads/allimg/200503/234040-15885204403184.jpg
        name = image_names[i].replace(r":","_").replace(r"/","_").replace('\\',"_").replace(r"*"," ").replace(r"<"," ").replace(r">"," ").replace(r"?"," ").replace(r"|","_")
        try:
            with open(path + '/' + name + '.jpg', mode="wb") as f:
                f.write(real_response.content)
            f.close()
            print(image_names[i] + "----------------下载完毕！")
        except Exception as error:
            print(error)
    print("----------------------第{}页图片下载完毕！----------------------".format(page),'\n')

if __name__ == '__main__':
    for i in range(1,10):
        if (i == 1):
            url = 'http://pic.netbian.com/4kdongman/'
            download_images(i,url)
        else:
            url = 'http://pic.netbian.com/4kdongman/index_' + str(i) + '.html'
            download_images(i,url)
            time.sleep(3)