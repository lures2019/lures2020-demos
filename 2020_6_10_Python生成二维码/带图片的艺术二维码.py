from MyQR import myqr
import os

path = "生成的二维码"
if not os.path.exists(path):
    os.mkdir(path)
myqr.run("https://www.bilibili.com/video/BV1ef4y1m7Zs",picture="Sources/害羞.png",colorized=True,save_name="带图片的艺术二维码彩色版.png", save_dir=path)