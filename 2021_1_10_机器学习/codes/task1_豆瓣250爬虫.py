"""
    ### 实验三、网络爬虫（25"）

- 1、爬取所有豆瓣电影评分`Top250`的电影的信息`（10"）`
  - a）正文链接
  - b）英文名（如有），中文名
  - c）其他信息
"""
import requests
import parsel
import re
import csv
import os


# 获取每页的信息
def extract_information(url):
    # 添加请求头信息，伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    # 使用parsel补全HTML
    select = parsel.Selector(response.text)
    links = []  # 电影评价正文链接
    titles_ZH = []  # 电影中文名称
    titles_EH = []  # 电影英文名称
    directors = []  # 导演
    stars = []  # 主演
    years = []  # 上映时间
    first_areas = []  # 首映地区
    types = []  # 电影类型
    scores = []  # 评分
    comment_persons = []  # 评价人数
    summarys = []  # 一句话总结
    lis = select.xpath('//ol[@class="grid_view"]/li/div[@class="item"]')
    # 开始二次提取
    for i in range(len(lis)):
        links.append(lis[i].xpath('//div[@class="pic"]/a/@href').getall()[i])
        titles_ZH.append(lis[i].xpath('//div[@class="info"]/div[@class="hd"]/a/span[@class="title"][1]/text()').getall()[i])
        # 输出显示有 \xa0/\xa0   需要字符串处理，且数目是22，不是25，有缺失，通过判断第二个span标属性来判断
        title_num = lis[i].xpath('//div[@class="info"]/div[@class="hd"]/a/span[2]').getall()[i]
        # 若属性是title则是我们想要的
        if "title" in title_num:
            # 使用正则表达式进行提取
            title = re.findall('<span class="title"> / (.*?)</span>', title_num)[0]
            titles_EH.append(title)
        else:
            titles_EH.append("无对应英文名称！")
        actors = lis[i].xpath('//div[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]').getall()[i]
        directors.append(actors.split("主演:")[0].split("导演:")[-1].strip())
        stars.append(actors.split("主演:")[-1])
        # 这边倒是新用法，不常见text()[2]
        others = lis[i].xpath('//div[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').getall()[i].split('/')
        years.append(others[0].replace("\n", "").strip())
        first_areas.append(others[1].replace("\n", "").strip())
        types.append(others[2].replace("\n", "").strip())
        scores.append(lis[i].xpath('//div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').getall()[i])
        comment_persons.append(lis[i].xpath('//div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[4]/text()').getall()[i])
        try:
            summarys.append(lis[i].xpath('//div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()').getall()[i])
        except Exception as error:
            # 跪了，哈利波特居然没有
            summarys.append("无")
    return links,titles_ZH,titles_EH,directors,stars,years,first_areas,types,scores,comment_persons,summarys


if __name__ == '__main__':
    # 创建文件夹
    path = '爬取的数据'
    # 不存在此目录，则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    # 创建csv文件用于保存豆瓣250数据
    f = open(path + '/' + "豆瓣250电影简略信息.csv",mode="w",encoding='utf-8-sig',newline="")
    csv_write = csv.writer(f)
    csv_write.writerow(['中文名称','英文名称','导演','主演','上映时间','首映地区','类型','评分','评价人数','一句话总结','链接'])
    # 不关闭，后面写入有问题
    f.close()
    # 开始爬取
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(25 * i)
        # 打开已创建的文件
        fp = open(path + '/' + '豆瓣250电影简略信息.csv',mode='a+',encoding='utf-8-sig',newline="")
        csv_write = csv.writer(fp)
        # 类的初始化
        links, titles_ZH, titles_EH, directors, stars,years,first_areas,types, scores, comment_persons, summarys = extract_information(url)
        for j in range(len(links)):
            csv_write.writerow([titles_ZH[j], titles_EH[j], directors[j], stars[j],years[j],first_areas[j],types[j],scores[j], comment_persons[j], summarys[j],links[j]])
        print("第{}页信息已写入文件！".format(i+1))



