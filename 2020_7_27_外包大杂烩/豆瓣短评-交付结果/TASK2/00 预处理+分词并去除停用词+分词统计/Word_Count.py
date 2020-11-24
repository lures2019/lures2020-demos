#!/usr/bin/python
# -*- coding: UTF-8 -*-

import jieba

str00 = input("选择分词工具<1: JIEBA, 2: NLPIR, 3: THULAC, 4: Stanford>:")


def txt():  # 输出词频前N的词语
    txt = open("yiqing.txt", "r", encoding='utf-8').read()  # 打开txt文件,要和python在同一文件夹
    txt00 = open("shuchu01.txt", "a+", encoding='utf-8')
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
    items = list(counts.items())  # 返回所有键值对
    items.sort(key=lambda x: x[1], reverse=True)  # 降序排序
    N = eval(input("请输入N：代表输出的数字个数："))
    wordlist = list()
    for i in range(N):
        word, count = items[i]
        txt00.write("{0:<10}{1:<5}".format(word, count))  # 输出前N个词频的词语
        txt00.write('\n')
    txt00.close()


if str00 == '1':
    txt()
    print('成功！')
elif str00 == '2':
    pass
    print('这是 pass 块')
elif str00 == '3':
    pass
    print('这是 pass 块')
elif str00 == '4':
    pass
    print('这是 pass 块')
else:
    pass
    print('这是 pass 块!!!!')
