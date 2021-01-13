"""
    - 3、加分项：
      - a）不限于豆瓣的简介，影评
      - b）是否分析了演员与电影类型的关联程度
      - c）是否分析了演员与演员的关系？
      - d）是否对简介和影评进行词云分析？
      - e）其他信息
"""
"""
    根据爬下来的评论数据，绘制词云图
"""
import os
import jieba
import cv2
import csv
from wordcloud import WordCloud


def make_cloud(path,comments,name):
    text = " ".join(i for i in comments)
    cut_text = " ".join(jieba.cut(text))
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
        # font_path=path.join(d,'simsun.ttc'),
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=500,
        # 最大号字体
        max_font_size=40
    )
    wCloud = cloud.generate(cut_text)
    # 保存图片到path路径下
    wCloud.to_file(path + '/' + '{}.jpg'.format(name))

# 需要将生成的词云图片放到对应的子目录下
path = '爬取的数据'
f = open(path + '/' + "豆瓣250电影信息.csv",mode='r',encoding='utf-8')
csv_reader = csv.reader(f)
rows = [i for i in csv_reader]
# 去除第一行后，每行的最后一列就是评论内容
comments = [row[-1] for row in rows[1:]]
instruction = [row[-2] for row in rows[1:]]
make_cloud(path,comments,"短评")
make_cloud(path,instruction,"简介")
