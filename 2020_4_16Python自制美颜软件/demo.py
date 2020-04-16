from tkinter import *
import cv2          # pip install opencv-python
from tkinter import messagebox
import os


def fix_photo():
    content = entry.get()
    con = content.strip()
    name = con.split(r'.')[0].split(r'/')[-1]
    if con == "":
        messagebox.showinfo("提示","请输入正确的照片的路径！")
    else:
       try:
           image = cv2.imread(con)
           value = 40
           # value是美颜程度，值越大程度越大，值越小程度越小
           image_dst = cv2.bilateralFilter(image, value, value * 2, value / 2)
           # 把美颜后的效果生成一张照片
           path = 'photos_after_beauty'
           if not os.path.exists(path):
               os.mkdir(path)
           cv2.imwrite(path + '/' + "%s.jpg" % (name), image_dst)
           messagebox.showinfo("提示", "图片已经美颜成功！")
       except EXCEPTION as error:
           pass
       # 自动清空输入框内容
       entry.delete(0,END)

window = Tk()
window.title("Python美颜工具1.0")
window.geometry("300x100+200+200")
window.resizable(0,0)
label = Label(window,text="图片地址：",font=("仿宋",12))
label.grid(row=0,column=0)
entry = Entry(window,width="28")
# entry不能和grid连写，否则会报错
entry.grid(row=0,column=1)
label2 = Label(window,text="").grid(row=1,column=0)
label3 = Label(window,text="").grid(row=2,column=0)
button1 = Button(window,text="开始美颜",font=("仿宋",12),command=fix_photo)
button1.grid(row=3,column=0)
button2 = Button(window,text="退出软件",font=("仿宋",12),command=window.quit)
button2.grid(row=3,column=1,sticky="e")
window.mainloop()

