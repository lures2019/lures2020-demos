#!/usr/bin/python
# -*- coding: UTF-8 -*-

import jieba

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import numpy as np
from PIL import Image


def txt():  # 输出词频前N的词语并且以str的形式返回
    txt = open("shuchu01.txt", "r", encoding='utf-8').read()  # 打开txt文件,要和python在同一文件夹
    words = jieba.lcut(txt)  # 精确模式，返回一个列表
    counts = {}  # 创建字典
    for word in words:
        if len(word) == 1:  # 把意义相同的词语归一
            continue
        elif word == "三炮" or word == "山炮":
            rword = "三炮"
        else:
            rword = word
        counts[rword] = counts.get(rword, 0) + 1  # 字典的运用，统计词频
    items = list(counts.items())  # 返回所有键值对P168
    items.sort(key=lambda x: x[1], reverse=True)  # 降序排序
    N = eval(input("请输入N：代表输出的数字个数"))
    wordlist = list()
    for i in range(N):
        word, count = items[i]
        #   print("{0:<10}{1:<5}".format(word, count))  # 输出前N个词频的词语
        wordlist.append(word)  # 把词语word放进一个列表
    a = ' '.join(wordlist)  # 把列表转换成str wl为str类型，所以需要转换
    return a


def create_word_cloud():
    wl = txt()  # 调用函数获取str！！
    # 图片名字 需一致
    cloud_mask = np.array(Image.open("love.jpg"))  # 词云的背景图，需要颜色区分度高

    wc = WordCloud(
        background_color="black",  # 背景颜色
        mask=cloud_mask,  # 背景图cloud_mask
        max_words=100,  # 最大词语数目
        font_path='simsun.ttf',  # 调用font里的simsun.tff字体，需要提前安装
        height=1200,  # 设置高度
        width=1600,  # 设置宽度
        max_font_size=1000,  # 最大字体号
        random_state=1000,  # 设置随机生成状态，即有多少种配色方案
    )

    myword = wc.generate(wl)  # 用 wl的词语 生成词云
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('1.jpg')  # 把词云保存下当前目录（与此py文件目录相同）


if __name__ == '__main__':
    create_word_cloud()
