from MyQR import myqr
import os

path = "生成的二维码"
if not os.path.exists(path):
    os.mkdir(path)
myqr.run("https://www.bilibili.com/video/BV1ef4y1m7Zs",picture="Sources/gakki.gif",colorized=True,save_name="动态二维码.gif", save_dir=path)