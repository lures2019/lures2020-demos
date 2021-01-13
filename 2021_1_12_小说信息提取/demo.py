import requests
from lxml import etree


def get_information(url):
    url = url
    # 构造请求头，模拟浏览器操作
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    # 获取响应
    response = requests.get(url, headers=headers)
    # 获取到网页信息
    html = response.text
    parse = etree.HTMLParser(encoding='utf-8')
    # 解析返回的响应结果
    select = etree.HTML(html)
    # 构造xpath提取规则，一次提取得到所有div信息
    divs = select.xpath('//div[@id="catalog"]/div')
    # 打开文件
    f = open("小说信息.txt",mode='a+',encoding='utf-8')
    # 二次提取
    for i in range(len(divs)):
        # 小说名称
        title = divs[i].xpath('./span[@class="title"]/a/text()')[0]
        # 小说简介
        introduction = divs[i].xpath('./div[1]/text()')[0].replace("\n", "").strip()
        # 小说作者
        author = divs[i].xpath('./div[2]/span/text()[2]')[0].replace("\n", "").strip()
        # 开始写入文件
        f.write("{}|{}|{}".format(title,author,introduction))
        f.write("\n")
    f.close()

if __name__ == '__main__':
    # 循环开始
    for page in range(1,11):
        url = 'http://www.ijjxsw.com/txt/Xuanhuan/index_{}.html'.format(page)
        get_information(url)