import os
import shutil


# 原始数据集文件相对路径
dst_path = '../datasets/archive'
# 文件集合
files = os.listdir(dst_path)
# 获取所有文件的前两个字母，用于创建子文件夹
names = []
for file in files:
    my_str = file[:2]
    if my_str in names:
        pass
    else:
        names.append(my_str)
# print(names)
# 在当前路径下创建以names为名称的子文件夹
for name in names:
    path = dst_path + '/' + name
    # 若不存在此目录则自动创建一个
    if not os.path.exists(path):
        os.mkdir(path)
    # 开始将对应字母开头的文件存入到对应的文件夹下
    for file in files:
        if name == file[:2]:
            shutil.move(dst_path + '/' + file,path)
        else:
            pass
