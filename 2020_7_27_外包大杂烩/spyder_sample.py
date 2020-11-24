"""
    开发一个爬虫，要求选取任意站点(百度或者豆瓣)获取站点的信息列表，要求文本数据50条以上。音频或视频不限，做简单的数据分析
    思路：
        Python爬取豆瓣250电影评分信息进行数据可视化展示
"""
import requests
import parsel
import time
import matplotlib.pyplot as plt

def get_message(url):
    url = url
    headers = {
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/top250?start=50&filter=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    select = parsel.Selector(response.text)
    scores = select.xpath('//ol[@class="grid_view"]/li/div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').getall()
    return(scores)

if __name__ == '__main__':
    scores_all = []
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(25*i)
        scores = get_message(url)
        for j in range(len(scores)):
            scores_all.append(scores[j])
        time.sleep(2)
    # 最高分9.7，最低分8.3
    score_dict = {}
    for score in scores_all:
        if score not in score_dict:
            score_dict[score] = 1
        else:
            score_dict[score] += 1
    keys = []
    values = []
    for key,value in score_dict.items():
        keys.append(key)
        values.append(value)
    plt.plot(keys,values)
    plt.xlabel('score')
    plt.ylabel('numbers')
    plt.title('douban250')
    plt.show()