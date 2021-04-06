import os
# 使用pandas切割数据
import pandas as pd


dst_path = '../datasets/archive'
# 这边获取的是各个子文件夹的名称
paths = os.listdir(dst_path)
# 需要依次遍历这些目录，寻找以.csv为后缀的文件
for path in paths:
    path_now = dst_path + '/' + path
    # 各个子目录下面文件组成的列表
    names = os.listdir(path_now)
    for name in names:
        # 这边就匹配到各自对应的csv文件了
        if name.split(".")[0] == path + 'videos_out':
            try:
                # 打开对应文件
                data = pd.read_csv(path_now + '/' + name,encoding='latin-1')
                # 开始切割
                num = 0
                for i in range(4):
                    start = num
                    num += int(data.shape[0] / 4)
                    file = data.iloc[start:num,]
                    file.to_csv(path_now + '/' + name.split(".")[0] + str(i) + '.csv',index=False)
                print('{}开始分隔完毕！'.format(name))
            except Exception as error:
                print("{}-----------------{}".format(name,error))