import requests
import json
import pandas as pd

def get_url(i):
    # 根据xhr提取出的真实url
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=recommend&page_limit=20&page_start={}'.format(20 * i)
    # 构造请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    # 设置编码和解码
    response.encoding = response.apparent_encoding
    # 提取出json格式数据
    texts = json.loads(response.text)['subjects']
    # 将电影名存储到一个列表中
    movie_names = []
    for text in texts:
        movie_names.append(text['title'])
    # 打印电影名称
    print(movie_names)

    # 使用pandas将电影名称存储到excel表格
    # 将列表转成dataframe
    df = pd.DataFrame(movie_names, columns=['电影名称'])
    # 保存到本地excel,追加写入,解决乱码
    df.to_csv("电影名称.csv", mode="a+",encoding="utf-8-sig",index=False)


if __name__ == '__main__':
    # 以10页为例
    for i in range(25):
        get_url(i)
        # 默认20个加载一次
        print("已加载{}项".format(20 * (i + 1)))

