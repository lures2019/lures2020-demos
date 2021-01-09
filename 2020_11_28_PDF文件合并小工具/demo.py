"""
    功能：1）可以通过鼠标形式勾选想要处理的文件夹
         2）可以选择性合并多个pdf文件
         3）可以通过鼠标形式导出到相应的目录
"""
from tkinter import *
from tkinter.filedialog import askopenfilenames,asksaveasfilename
from tkinter import messagebox
import threading
from PyPDF2 import PdfFileReader, PdfFileWriter

# 1、添加选择目标文件集，以元组形式返回所有的文件名
def selectPath():
    my_list = []
    path_ = askopenfilenames()
    path.set(path_)
    my_list.append(path_)
    return my_list

# 2、添加多线程，避免界面卡顿
def thread_it(func):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()

# 3、添加窗口说明菜单
def about():
    messagebox.showinfo('提示', '本应用写于2020年11月28日，制作人lures！')

# 4、添加保存pdf到目标目录
def savePdf():
    my_list = []
    path_ = asksaveasfilename()
    save.set(path_)
    my_list.append(path_)
    return my_list

# 5、添加pdf合并功能
def merge():
    # 手动选择输出文件的路径
    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = savePdf()[0]
    my_list = selectPath()
    # [('D:/lures2020-demos/2020_12_神经网络与深度学习Tensorflow2.0实战/课件/0 课程概述.pdf', 'D:/lures2020-demos/2020_12_神经网络与深度学习Tensorflow2.0实战/课件/1.1 人工智能的诞生.pdf')]
    # 以元组的形式呈现，my_list[0][0]/my_list[0][1]这样获取每一个pdf文件
    for i in range(len(my_list[0])):
        # 读取源pdf文件
        input_file = PdfFileReader(open(my_list[0][i],"rb"))
        # 获得源pdf文件中页面总数
        pageCount = input_file.getNumPages()
        outputPages += pageCount
        # 分别将page添加到输出output中
        for ipage in range(pageCount):
            output.addPage(input_file.getPage(ipage))
    outputStream = open(pdf_fileName,"wb")
    output.write(outputStream)
    outputStream.close()
    messagebox.showinfo("提示！","完成合并！祝您生活愉快~")

# 6、添加使用说明文件
def use_function():
    messagebox.showinfo('提示', '使用说明如下：\n首先，需要选择合并PDF后保存的路径及名称（记为：text）\n其次，会弹出一个框让你选择一个要合并的多个PDF文件\n最后，完成合并后会在目标目录生成text\n完成合并后，会弹出一个框显示已经完成合并')

# 开始构造整体框架
if __name__ == '__main__':
    root = Tk()
    path = StringVar()
    save = StringVar()              # 保存路径
    root.title("PDF合并小工具")
    root.geometry('370x120+800+400')
    root.resizable(0, 0)
    # 显示内容部分
    label1 = Label(root, text='目标路径:', font=("仿宋", 12)).grid(row=0, column=0, sticky='e')
    entry1 = Entry(root, textvariable=path, width='30').grid(row=0, column=1)
    label2 = Label(root, text='保存路径:', font=("仿宋", 12)).grid(row=1, column=0, sticky='e')
    entry2 = Entry(root, textvariable=save,width='30').grid(row=1, column=1)
    Label(root, text="").grid(row=2, column=1)
    button1 = Button(root, text="合并PDF", font=("仿宋", 12), command=lambda :thread_it(merge)).grid(row=3, column=0,sticky='e')
    button2 = Button(root, text="退出Exit", font=("仿宋", 12), command=root.quit).grid(row=3, column=2, sticky='w')
    label3 = Label(root, text="lures友情出品，欢迎致电2142781703~~~", font=("仿宋", 10)).grid(row=4, columnspan=3, sticky='e')
    # 添加窗口栏菜单
    menu1 = Menu(root)
    menu1.add_command(label="About", command=about)
    menu1.add_command(label="使用说明", command=use_function)
    root.config(menu=menu1)
    root.mainloop()
