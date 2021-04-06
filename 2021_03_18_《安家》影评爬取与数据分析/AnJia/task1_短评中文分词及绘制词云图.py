import jieba
import jieba.analyse
import re
import cv2
from wordcloud import WordCloud
import os

# 首先获取json文件的所有短评信息
def get_datas_from_json():
    f = open('《安家》短评.json',mode='r',encoding='utf-8')
    datas = f.read()
    comments = re.findall("comments\": (.*?)\n",datas)
    my_str = ""
    for comment in comments:
        my_str += comment
    return my_str

# 使用jieba进行分词
def get_jieba():
    string = get_datas_from_json()
    # 去除string里面的标点符号
    text = re.sub('\W*', '',string)
    word_list = jieba.lcut(text)
    text_cut = ' '.join(word_list)
    return text_cut

# 绘制词云图
def draw_wordcloud(path):
    # 导入停词
    # 用于去掉文本中类似于'啊'、'你'，'我'之类的词
    words = get_jieba()
    stop_words = open("stop_words_zh.txt", encoding="utf8").read().split("\n")
    # 使用WordCloud生成词云
    color_mask = cv2.imread('mask.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path = " C:\\Windows\\Fonts\\STXINGKA.TTF",
        # 设置背景色
        background_color = 'white',
        # 词云形状
        mask = color_mask,
        # 允许最大词汇
        max_words = 500,
        # 最大号字体
        max_font_size = 40,
        stopwords = stop_words
    )
    wCloud = cloud.generate(words)
    wCloud.to_file(path + '/' + '《安家》短评词云图.jpg')

if __name__ == "__main__":
    path = "pictures"
    # 没有此目录则创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    draw_wordcloud(path)

