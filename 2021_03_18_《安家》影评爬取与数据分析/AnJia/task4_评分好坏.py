import re
import matplotlib.pyplot as plt
import os

# 首先获取json文件的所有短评信息
def get_datas_from_json():
    f = open('《安家》短评.json',mode='r',encoding='utf-8')
    datas = f.read()
    ratings = re.findall("rating\": (.*?),\n",datas)
    # 获取rating列表
    ratings_list = []
    for rating in ratings:
        # ratings_list.append(eval(rating))
        try:
            if len(eval(rating)) == 2:
                ratings_list.append(eval(rating))
            else:
                ratings_list.append('放弃')
        except Exception as e:
            ratings_list.append('放弃')
    return ratings_list


# 绘制柱状图
def draw_histogram():
    ratings = get_datas_from_json()
    my_dict = {}
    for rating in ratings:
        if rating not in my_dict:
            my_dict[rating] = 1
        else:
            my_dict[rating] += 1
    keys = list(my_dict.keys())
    values = list(my_dict.values())
    plt.figure(figsize=(10, 5))
    # 设置显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(range(len(keys)), values, color=['b', 'r', 'g', 'y', 'c', 'm', ])
    plt.xticks(range(len(keys)), keys, fontsize=15)
    plt.yticks(fontsize=15)
    plt.savefig(path + '/' + '《安家》推荐版柱状图.jpg')
    plt.show()


if __name__ == "__main__":
    path = "pictures"
    if not os.path.exists(path):
        os.mkdir(path)
    draw_histogram()