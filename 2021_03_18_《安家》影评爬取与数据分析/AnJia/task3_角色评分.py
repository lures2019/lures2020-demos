import jieba.analyse
import re
import matplotlib.pyplot as plt
import pandas as pd
import os


# 首先获取json文件的所有短评信息
def get_datas_from_json():
    f = open('《安家》短评.json',mode='r',encoding='utf-8')
    datas = f.read()
    comments = re.findall("comments\": (.*?),\n",datas)
    ratings = re.findall("rating\": (.*?),\n",datas)
    # 获取评论信息列表
    comments_list = []
    for comment in comments:
        comments_list.append(eval(comment if "null" else ""))
    # 获取rating列表
    ratings_list = []
    for rating in ratings:
        # ratings_list.append(eval(rating))
        try:
            if len(eval(rating)) == 2:
                ratings_list.append(eval(rating))
            else:
                ratings_list.append(0)
        except Exception as e:
            ratings_list.append(0)
    # 去除rating无用数据对应的评论数据
    new_comments = []
    new_ratings = []
    for i in range(len(ratings_list)):
        if ratings_list[i] == 0:
            pass
        else:
            new_comments.append(comments_list[i])
            new_ratings.append(ratings_list[i])
    return new_ratings,new_comments


if __name__ == "__main__":
    path = "pictures"
    if not os.path.exists(path):
        os.mkdir(path)
    # 力荐：+5，推荐：+4，还行：3，较差：2，很差：1
    roles = {
        '房似锦': 0,
        '徐文昌': 0,
        '张乘乘': 0,
        '王子健': 0,
        '楼山关': 0,
        '朱闪闪': 0,
        '谢亭丰': 0,
        '鱼化龙': 0,
        '宫蓓蓓': 0,
        '阚文涛': 0
    }
    role_names = list(roles.keys())
    for name in role_names:
        jieba.add_word(name)
    ratings,comments = get_datas_from_json()
    for i in range(len(comments)):
        content = comments[i]
        rating = ratings[i]
        words = list(jieba.cut(content,cut_all=False))
        # 返回一个新集合，该集合的元素既包含在集合 role_name 又包含在集合 words 中
        names = set(role_names).intersection(set(words))
        for name in names:
            if rating == '力荐':
                roles[name] += 5
            elif rating == '推荐':
                roles[name] += 4
            elif rating == '还行':
                roles[name] += 3
            elif rating == '较差':
                roles[name] += 2
            elif rating == '很差':
                roles[name] += 1
    role_df = pd.DataFrame(list(roles.values()), index=list(roles.keys()), columns=['得分'])
    # 创建一个画布，并指定宽高
    plt.figure(figsize=(15, 8))
    # 设置显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 绘制一个柱状图
    plt.bar(role_df.index, role_df.values.flatten(), color='b')
    # 设置坐标中字体大小
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    # 保存图形
    plt.savefig(path + '/' + '《安家》角色评分柱状图.jpg')
    # 显示图形
    plt.show()
