import requests
import parsel
import redis
import json

def get_url(url):
    session = requests.Session()
    headers = {
        'referer': 'https://blog.csdn.net/weixin_43862765/article/list/2',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    response = session.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    select = parsel.Selector(response.text)
    # 文章的标题
    titles = select.xpath(
        '//div[@class="article-list"]/div[@class="article-item-box csdn-tracking-statistics"]/h4/a/text()')
    # 文章的链接
    title_urls = select.xpath(
        '//div[@class="article-list"]/div[@class="article-item-box csdn-tracking-statistics"]/h4/a/@href').getall()
    title = []
    for i in range(len(titles)):
        # 去除不必要的信息
        if (i % 2) != 0:
            title.append(titles[i].get().strip())
        else:
            pass
    update_times = select.xpath(
        '//div[@class="article-list"]/div[@class="article-item-box csdn-tracking-statistics"]/div[@class="info-box d-flex align-content-center"]/p/span[@class="date"]/text()')
    # 文章上传时间
    time = []
    for i in range(len(update_times)):
        time.append(update_times[i].get().strip())
    # 阅读数和评论数
    results = select.xpath(
        '//div[@class="article-list"]/div[@class="article-item-box csdn-tracking-statistics"]/div[@class="info-box d-flex align-content-center"]/p/span[@class="read-num"]/span[@class="num"]/text()')
    read_nums = []
    comment_nums = []
    for j in range(len(results)):
        if (j % 2 == 0):
            read_nums.append(results[j].get())
        else:
            comment_nums.append(results[j].get())
    connection = redis.Redis(host="localhost", port=6379, db=0)
    for i in range(len(title)):
        str = title[i] + '\t' + time[i] + '\t' + read_nums[i] + '\t' + comment_nums[i] + '\t' + title_urls[i]
        connection.rpush("文章详情", str)

if __name__ == '__main__':
    for i in range(1,4):
        url = 'https://blog.csdn.net/weixin_43862765/article/list/' + str(i)
        get_url(url)
        print("第{}页信息采集到redis数据库中！".format(i))