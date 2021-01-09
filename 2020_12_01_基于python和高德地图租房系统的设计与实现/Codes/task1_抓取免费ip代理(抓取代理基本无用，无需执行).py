"""
    抓取58同城房源数据时，ip被限制，需要爬取免费ip代理网站，打造ip代理池
"""
import requests
import parsel

url = 'https://www.feizhuip.com/news-getInfo-id-1274.html'
response = requests.get(url)
response.encoding = response.apparent_encoding
select = parsel.Selector(response.text)
ips = select.xpath('//tr/td[1]/text()').getall()
ports = select.xpath('//tr/td[2]/text()').getall()

# 将抓取到的ip存放到ip.txt文件中
f = open('ip.txt',mode='w',encoding='utf-8')
for i in range(len(ips)):
    f.write("{}:{}".format(ips[i],ports[i]))
    f.write('\n')
