"""
    想法：想通过阅读名家经典作品替代无脑的网文小说，于是打算爬取这个网站来收集一些文学大佬的作品
    网址：https://haoshu100.com/archives/category/%e6%96%87%e5%ad%a6/%e4%b8%ad%e5%9b%bd%e6%96%87%e5%ad%a6
"""
import requests
import parsel
import pdfkit
import os
import shutil

path = '中国文学著作'
if not os.path.exists(path):
    os.mkdir(path)

def download_one_page(url):
    url = url
    headers = {
        'Cookie': 'PHPSESSID=epgfag0ofm3b672nk3915296i0; Hm_lvt_18f208a35faf157dc0d260db85eedf6e=1593242079,1593242728; Hm_lpvt_18f208a35faf157dc0d260db85eedf6e=1593243002',
        'Host': 'haoshu100.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    html = response.text
    result = parsel.Selector(html)
    urls = result.xpath('//div[@class="fr box_content"]/h2/a/@href').getall()
    titles = result.xpath('//div[@class="fr box_content"]/h2/a/@title').getall()
    config = pdfkit.configuration(wkhtmltopdf=r"D:\python\pdfkit_wkhtmltox\wkhtmltopdf\bin\wkhtmltopdf.exe")
    for i in range(len(urls)):
        pdfkit.from_url(urls[i], titles[i] + '.pdf', configuration=config)
        shutil.move(titles[i] + '.pdf', path)

if __name__ == '__main__':
    for i in range(1,4):
        url = 'https://haoshu100.com/archives/category/%e6%96%87%e5%ad%a6/%e4%b8%ad%e5%9b%bd%e6%96%87%e5%ad%a6/page/{}'.format(i)
        download_one_page(url)