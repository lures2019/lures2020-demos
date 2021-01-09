"""
    根据爬下来的评论数据，绘制词云图
"""
import os
import jieba
import cv2
import csv
from wordcloud import WordCloud, STOPWORDS
from string import digits


def make_cloud(path,comments):
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
    wCloud.to_file(path + '/' + 'cloud.jpg')

# 需要将生成的词云图片放到对应的子目录下
paths = ['中国医学史', '北大张大庆', '思政课', '文化自信', '黑龙江常存库']
for path in paths:
   file_list = os.listdir(path)
   if len(file_list) == 1:
       f = open(path + '/' + file_list[0],mode='r',encoding='utf-8')
       csv_reader = csv.reader(f)
       rows = [i for i in csv_reader]
       # 去除第一行后，每行的第一列就是评论内容
       comments = [row[0] for row in rows[1:]]
       make_cloud(path,comments)
   else:
       # 默认第一个也是 评论.csv
       f = open(path + '/' + file_list[0], mode='r', encoding='utf-8')
       csv_reader = csv.reader(f)
       try:
           rows = [i for i in csv_reader]
           # 去除第一行后，每行的第一列就是评论内容
           comments = [row[0] for row in rows[1:]]
           make_cloud(path, comments)
       except Exception as error:
           print(error)