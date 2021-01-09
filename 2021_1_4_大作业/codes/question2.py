"""
    利用Jieba库，进行词频统计，要求不能使用课堂上例子，并且所使用的文章不能低于100页（可以是一些长篇小说，日轻，青春小说的
        txt文本，测试文本字号为小四）
"""
import jieba
import re

# 使用    99青春·青春小说《毕业后，我们一起淘金》.txt 作为分析文本
article = open("99青春·青春小说《毕业后，我们一起淘金》.txt",mode='r')
# 使用正则表达式去除txt中的标点符号
text = re.sub('\W*', '', article.read())
# 采用精确模式进行匹配
words = jieba.cut(text,cut_all=False)
# 记录词频
word_dict = {}
for word in words:
    # 如果字典中不存在则赋值为1，否则自动+1
    if word not in word_dict:
        word_dict[word] = 1
    else:
        word_dict[word] += 1
# 开始按照词出现的次数进行排列
print(sorted(word_dict,key=lambda k:word_dict[k],reverse=True))
