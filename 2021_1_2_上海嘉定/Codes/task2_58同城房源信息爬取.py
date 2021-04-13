import requests
from lxml import etree
import csv
from multiprocessing import Pool


def get_information(url):
    url = url
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'cookie': 'f=n; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; userid360_xml=37C9779F851E78C1C4B303978DE876CF; time_create=1612177230149; id58=c5/nfF/EZ7K9szlhIdRtAg==; 58tj_uuid=a89d7ee0-11b7-4dfa-b6d3-13d1b9a2124f; als=0; wmda_uuid=2858ccc1c7f8d48bd768901920860bb7; wmda_new_uuid=1; xxzl_deviceid=BLAsSIJvtTC3Fux0oeRXTrKOJT2KR1yvH%2BBElfTfBvRqQBW0V1VndrR7hTywSoPp; __utma=253535702.1807371373.1606707139.1606709695.1606735330.3; __utmz=253535702.1606735330.3.3.utmcsr=qhd.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/; xxzl_smartid=6a52d21fdbd69c5126d8bcdd0efcf84e; wmda_visited_projects=%3B11187958619315%3B10104579731767%3B2385390625025; f=n; 58home=sh; city=sh; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; commontopbar_ipcity=qhd%7C%E7%A7%A6%E7%9A%87%E5%B2%9B%7C0; crmvip=""; dk_cookie=""; www58com="UserID=61109356394512&UserName=fx5s82v5k"; 58cooper="userid=61109356394512&username=fx5s82v5k"; 58uname=fx5s82v5k; ppStore_fingerprint=4D39984CE9573D3D5E8DAAC6C140624AA23DAD05CC387BB4%EF%BC%BF1609587842767; new_uv=11; utm_source=; spm=; init_refer=https%253A%252F%252Fcallback.58.com%252Fantibot%252Fverifylogin%253FserialId%253Da98c760f0efa7d3599c1a79e6076560a_8c29f4a85ec44cb1bcf002d9176eedb7%2526code%253D-5%2526sign%253Db8c1c375cac36a8e062655311504d95c%2526namespace%253Dzufanglistphp%2526url%253Dhttps%25253A%25252F%25252Fjiading.58.com%25252Fchuzu%25252F%2526platform%253Dpc; wmda_session_id_11187958619315=1609594044684-79de69af-9b38-3fa5; new_session=0; PPU=UID=61109356394512&UN=fx5s82v5k&TT=f6a58a45d34e9eca204e85827e8b0ec4&PBODY=RMFf_VzFY_8nRxApQgrC7p8RGL5kJ_d4P3QH1d3AVxsw71PLrX_nGtYlHYGojud5B5z_hKSaecydPDhWYhLTjPzQecGUHrfhpb8TgODqkgov0YN4bgCgSvF3QsRMiYi-8Mlb1jBy-AWLKJifZS1X5T9GzF_vSIoznmh_P7TspUw&VER=1; xxzl_cid=4c03644d5b6940f1b957d754fac7d38e; xzuid=76999865-5470-414a-8322-b06605672899'
        }
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text, etree.HTMLParser())
        # 开始提取有用信息
        img_urls = html.xpath(
            '//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="img-list"]/a/@href')
        titles = html.xpath(
            '//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="des"]/h2/a/text()')
        communitys = html.xpath(
            '//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="des"]/p[@class="infor"]/a[2]/text()')
        prices = html.xpath(
            '//div[@class="list-wrap"]/div[@class="list-box"]/ul[@class="house-list"]/li/div[@class="list-li-right"]/div[@class="money"]/b/text()')
        """
            以首页链接为例：
                img_urls：图片链接   提取到98个信息
                titles：房屋名称     提取到97个信息
                communitys：小区名称 提取到97个信息
                prices：房价信息     提取到97个信息
            相关的列表集合需要对元素进行修改
            和之前相比，58同城去除了字体加密！！！（为啥要去掉？？？）
        """
        return img_urls, titles, communitys, prices
    except Exception as e:
        get_information(url)

def save_data_to_csv(url):
    url = url
    img_urls, titles, communitys, prices = get_information(url)
    img_urls_now = [url.split('?')[0] for url in img_urls]
    titles_now = []
    for title in titles:
        x = title.replace('\n', '').strip()
        if len(x) > 0:
            titles_now.append(x)
    # 所有的列表长度都是95
    return titles_now, communitys, prices, img_urls_now

# 4、开启多进程
def main(url):
<<<<<<< HEAD
<<<<<<< HEAD
    f = open("深圳龙华房源信息.csv",mode='a+',encoding='utf-8-sig',newline="")
=======
    f = open("上海嘉定房源信息.csv",mode='a+',encoding='utf-8-sig',newline="")
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
=======
    f = open("上海嘉定房源信息.csv",mode='a+',encoding='utf-8-sig',newline="")
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
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
<<<<<<< HEAD
<<<<<<< HEAD
            url = 'https://sz.58.com/szlhxq/chuzu/?minprice=2000_4000&sourcetype=5'
            urls.append(url)
        else:
            url = 'https://sz.58.com/szlhxq/chuzu/pn{}/?minprice=2000_4000&sourcetype=5'.format(j)
=======
=======
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
            url = 'https://sh.58.com/jiading/chuzu/'
            urls.append(url)
        else:
            url = 'https://sh.58.com/jiading/chuzu/pn{}/'.format(j)
<<<<<<< HEAD
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
=======
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
            urls.append(url)
    pool.map(main, urls)
    pool.close()
    pool.join()
<<<<<<< HEAD
<<<<<<< HEAD
    print("爬取完毕！")
=======
    print("爬取完毕！")
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
=======
    print("爬取完毕！")
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
