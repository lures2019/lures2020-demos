"""
    人工智能与传统美学绝妙搭配
"""
# jieba库用来进行中文分词
import jieba
from pyecharts.charts import Bar
from pyecharts.globals import CurrentConfig
# 本地的echarts.min.js文件所在位置，在线打开不行
CurrentConfig.ONLINE_HOST = "D:/python/Lib/site-packages/"
import win32com.client as wc

# 读取小说文件
file = open("三国演义.txt",mode="r",encoding="utf-8").read()
words = jieba.lcut(file)
speak = wc.Dispatch("SAPI.SpVoice")
speak.Speak(file)

# 特征提取
counts = {}
for word in words:
    if len(word) == 1:
        continue            # 筛选掉语气助词以及标点符号
    else:
        if counts.get(word) == None:
            counts[word] = 1
        else:
            counts[word] += 1
items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)

# 词语
word_list = []
# 频次
count_list = []

for i in range(15):
    word,count = items[i]
    word_list.append(word)
    count_list.append(count)

bar = Bar()
bar.add_xaxis(word_list)
bar.add_yaxis("三国演义风云榜",count_list)
bar.render("三国演义.html")