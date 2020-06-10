from MyQR import myqr
import os

path = "生成的二维码"
if not os.path.exists(path):
    os.mkdir(path)
myqr.run("https://www.bilibili.com/video/BV1ef4y1m7Zs",save_name="普通二维码.png", save_dir=path)