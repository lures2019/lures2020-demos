import os
import csv
from shutil import move
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing import image
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from tqdm import tqdm



# 1、使用字典统计  question2_result.csv里面的各个lab_status的数量
def get_different_labs():
    labs_dict = {}
    f = open("datas/question2_result.csv",mode="r",encoding="utf-8")
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    labs = [row[-1] for row in rows[1:]]
    for lab in labs:
        if lab not in labs_dict:
            labs_dict[lab] = 1
        else:
            labs_dict[lab] += 1
    # {'Positive ID': 14, 'Negative ID': 3194, 'Unverified': 86, 'Unprocessed': 11}
    print("处理前：{}".format(labs_dict))


# 2、遍历csv文件，判断FileType下只jpg和png格式的4种图片的数量，并将png都改成jpg形式
def choose_information():
    f = open("datas/question2_result.csv",mode='r',encoding="utf-8")
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    fp = open("datas/question2_3_information_fixing.csv",mode='w+',newline="",encoding="utf-8-sig")
    csv_write = csv.writer(fp)
    rows[0].append("lab_status")
    csv_write.writerow(rows[0])
    my_dict = {}
    for row in rows[1:]:
        form = row[-2].split("/")[-1]
        name = row[-2].split("/")[0]
        if (form == "jpg") or (form == "png") or (form == name):
            # 将png都改成jpg形式了
            if row[-1] not in my_dict:
                my_dict[row[-1]] = 1
            else:
                my_dict[row[-1]] += 1
            row[0] = row[0].replace("png","jpg")
            row[2] = row[2].replace("png","jpg")
            if form == name:
                row[0] = row[0] + ".jpg"
            csv_write.writerow(row)
        else:
            pass
    fp.close()
    print("处理后：{}".format(my_dict))


# 3、根据lab_status将files里面的图片复制到不同的数据集里面,并生成对应的csv文件
def divide_two_folders():
    """
        将lab_status是Unverified和Unprocessed放到测试集
        将lab_status是Positive ID和Negative ID分别作为训练集和验证集
    """
    path1 = "../2021MCM_ProblemC_Files/test_set"
    path2 = "../2021MCM_ProblemC_Files/train_set"
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    # 创建三个文件夹之后下面接着创建2个csv文件，分别放到对应文件夹下
    f1 = open(path1 + "/" + "test.csv",mode='w+',newline="",encoding="utf-8-sig")
    f2 = open(path2 + "/" + "train.csv",mode='w+',newline="",encoding="utf-8-sig")
    # 下面开始读取原先的csv文件
    fp = open("datas/question2_3_information_fixing.csv",mode='r',encoding="utf-8")
    csv_reader = csv.reader(fp)
    rows = [i for i in csv_reader]
    csv_write1 = csv.writer(f1)
    csv_write1.writerow(rows[0])
    csv_write2 = csv.writer(f2)
    csv_write2.writerow(rows[0])
    # 开始遍历文件
    # 处理后：{'Positive ID': 14, 'Negative ID': 3097, 'Unverified': 73, 'Unprocessed': 11}
    for row in rows[1:]:
        lab = row[-1]
        name = row[0]
        if (lab == "Unverified") or (lab == "Unprocessed"):
            # 删除最后一列lab_status
            del row[-1]
            csv_write1.writerow(row)
            # 根据name将文件剪切到对应文件夹下面
            src_path = "../2021MCM_ProblemC_Files/{}".format(name)
            try:
                move(src_path,path1)
            except Exception as error:
                print(error,name)
        else:
            # 将train和predict 按照7：3大致比例划分进对应的文件夹下面(一共3111张图片)
            if name == "ATT3151_Screenshot 2020-10-01 at 1.45.56 PM.jpg":
                pass
            else:
                if lab == "Positive ID":
                    row[-1] = 1
                else:
                    row[-1] = 0
                csv_write2.writerow(row)
            src_path = "../2021MCM_ProblemC_Files/{}".format(name)
            try:
                move(src_path, path2)
            except Exception as error:
                print(error,name)

    f1.close()
    f2.close()
    print("数据集划分完毕！")

# 4、开始模型的训练和验证
def train_and_predict():
    # 加载数据
    train = pd.read_csv('../2021MCM_ProblemC_Files/train_set/train.csv')
    # 将训练集的图片转成训练的数据
    # 我们将读取所有训练图像，将它们存储在列表中，最后将该列表转换为numpy数组。
    # 我们具有灰度图像，因此在加载图像时，我们将保持灰度 = True，如果您具有RGB图像，则应将灰度设置为False
    train_image = []
    for i in tqdm(range(train.shape[0])):
        img = image.load_img('../2021MCM_ProblemC_Files/train_set/' + train['﻿﻿﻿FileName'][i], target_size=(28, 28, 1), grayscale=True)
        img = image.img_to_array(img)
        img = img / 255
        train_image.append(img)
    X = np.array(train_image)
    # 由于这是一个多类分类问题（2个类），我们将对标签进行一次编码。
    y = train['lab_status'].values
    y = to_categorical(y)
    # 根据训练集划分出验证集
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)
    # 定义模型结构
    # 定义2个卷积层，1一个全连接的隐藏层和输出层
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

    # 训练模型
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
    # 预测数据
    # 读取预测的数据
    test = pd.read_csv('../2021MCM_ProblemC_Files/test_set/test.csv')
    test_image = []
    for i in tqdm(range(test.shape[0])):
        img = image.load_img('../2021MCM_ProblemC_Files/test_set/' + test['﻿﻿﻿FileName'][i], target_size=(28, 28, 1), grayscale=True)
        img = image.img_to_array(img)
        img = img / 255
        test_image.append(img)
    test = np.array(test_image)
    # 开始预测
    prediction = model.predict_classes(test)
    # 保持预测的结果
    sample = pd.read_csv('../2021MCM_ProblemC_Files/test_set/test.csv')
    sample['lab_status'] = prediction
    sample.to_csv('datas/test.csv', header=True, index=False)


if __name__ == "__main__":
    # get_different_labs()
    # choose_information()
    # divide_two_folders()
    train_and_predict()