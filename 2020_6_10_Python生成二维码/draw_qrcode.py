from MyQR import myqr
import os

path = "生成的二维码"
if not os.path.exists(path):
    os.mkdir(path)

def ordinary_qrcode(words,save_name):
    """普通二维码生成函数，传入参数：文本以及保存的图片名,如：("https://www.baidu.com","baidu.png")"""
    myqr.run(words=words,save_name=save_name,save_dir=path)

def color_qrcode(words,picture,save_name):
    myqr.run(words=words, picture=picture, colorized=True,save_name=save_name, save_dir=path)

def dynamic_qrcode(words,picture,save_name):
    myqr.run(words=words, picture=picture, colorized=True,save_name=save_name, save_dir=path)

