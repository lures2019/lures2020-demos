import numpy as np
from PIL import Image
import cv2


# 转为灰度图并转为01矩阵
def pretreatment(path):
    imge = Image.open(path)
    im = np.array(imge)
    # print(im)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i, j] == 0:
                im[i, j] = 1
            else:
                im[i, j] = 0
    return im


# 自动转为灰度图并转为01矩阵
def auto_pretreatment(img):
    X = []
    Y = []
    im1 = Image.open(img)
    imgi = im1.convert('1')
    im = np.array(imgi)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i, j] == 0:
                im[i, j] = 1
                X.append(j)
                Y.append(i)
            else:
                im[i, j] = 0
    min_X = min(X)-6
    max_X = max(X)+6
    min_Y = min(Y)
    max_Y = max(Y)
    img = imgi.crop((min_X, min_Y, max_X, max_Y)).resize((32, 32))
    img.save('images/text.png')
    im = np.array(img)
    # img.save(r'D:\py_work\Hello_world\numpy_test_pic\as.png')
    # np.savetxt(r'D:\py_work\Hello_world\numpy_test_pic\new.txt', img)
    return im


def save_pic_to_file(filename, path='images/text.png', mode=0):
    """
    :param filename:
    :param path:
    :param mode: 0为手动, 其他为自动模式
    :return:
    """
    # path = 'D:/ML_num/images/text.png'
    if mode == 0:
        ret = pretreatment(path)
    else:
        ret = auto_pretreatment(path)
    # for i in ret:
    #     print(i)
    np.savetxt('testDigits/{}.txt'.format(filename), ret, fmt='%d')
    with open('testDigits/{}.txt'.format(filename)) as f:
        num = f.read()
    if mode == 0:
        num = num.replace(' ', '')
    else:
        num = num.replace(' ', '').replace('1', '2').replace('0', '3').replace('2', '0').replace('3', '1')
    # print(num)
    with open('testDigits/{}.txt'.format(filename), 'w') as f:
        # print(num)
        f.write(num)


if __name__ == '__main__':
    save_pic_to_file('8_2', 'images/text.png')
