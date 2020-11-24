from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import subprocess as sub
import threading

top = Tk()
top.title("You-get视频下载器，made by @拼命三郎")

# 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央,其中width和height为界面宽和高
width = 555
height = 519
screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
top.geometry(alignstr)

# 阻止窗口调整大小
top.resizable(0, 0)
# 设置窗口图标
top.iconbitmap('logo.ico')

# 框架布局
frame_root = Frame(top)
frame_left = Frame(frame_root)
frame_right = Frame(frame_root)

frame_left.pack(side=LEFT)
frame_right.pack(side=RIGHT, anchor=N)
frame_root.pack()

# 输入视频链接
tip1 = Label(frame_left, text='请输入视频链接：         ', font=('楷体', 25))
tip1.pack(padx=10, anchor=W)
# 视频链接输入框
input_url = Entry(frame_left, bg='#F7F3EC')
input_url.pack(ipadx=159, ipady=8, padx=20, anchor=W)
# 请选择保存位置
tip2 = Label(frame_left, text='请选择保存位置：         ', font=('楷体', 25))
tip2.pack(padx=10, anchor=W)
# 保存地址输入框
input_save_address = Entry(frame_left, bg='#F7F3EC')
input_save_address.pack(ipadx=159, ipady=8, padx=20, anchor=W)


# 浏览本地文件夹，选择保存位置
def browse_folder():
    # 浏览选择本地文件夹
    save_address = filedialog.askdirectory()
    # 把获得路径，插入保存地址输入框（即插入input_save_address输入框）
    input_save_address.insert(0, save_address)


# 下载函数
def download():
    # 从输入框获取视频链接
    url = input_url.get()
    # 从输入框获取保存地址
    save_address = input_save_address.get()
    cmd = f'you-get   -o {save_address}   {url}'
    print(cmd)

    # 将cmd结果重定向到tkinterGUI，即将命令行的结果显示ScrolledText（滚动文本框）控件里
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    output = output.decode('UTF-8')
    stext.insert(END, output)
    # 使滚动文本框的滚动条始终保持在最底段
    stext.yview_moveto(1)


# 为避免在下载时tkinter界面卡死，创建线程函数
def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


# “浏览文件夹”按钮
browse_folder_button = Button(frame_right, text='浏览', font=('楷体', 15), command=lambda: thread_it(browse_folder))
browse_folder_button.pack(pady=110, side=LEFT, anchor=W)
# 新建空白标签，无实际作用，内容为空，为了让界面对称，更美观，可理解为“占位符”
Label(frame_right, text='     ').pack(pady=110, side=LEFT, anchor=W)

# “下载”按钮
download_button = Button(frame_left, text='下载', font=('楷体', 15), command=lambda: thread_it(download))
download_button.pack(padx=20, pady=6, anchor=W)

# ScrolledText组件（滚动文本框）
stext = ScrolledText(frame_left, width=60, height=23, background='#F7F3EC')
stext.pack(padx=20, anchor=W)

top.mainloop()
