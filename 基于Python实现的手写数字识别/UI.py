import os
import shutil
import tkinter.filedialog
import webbrowser
from tkinter import Tk, Label, Button, messagebox
from tkinter.simpledialog import askinteger

import check
import get_next_num
import hand_number
import kNN
import vedio_cut
import zero_one

root = Tk()
root.title('ML_number')
root.geometry('835x710+250+0')
root.resizable(False, False)


# 复制文件
def copy_file(filepath, tofilepath):
    path = filepath.replace('\\', '/')
    shutil.copy(path, tofilepath)


# 打开图像文件
def Open():
    filename = tkinter.filedialog.askopenfilename(title='Open Image',
                                                  filetypes=[('image', '*.png')])
    if filename:
        global image_src
        image_src = tkinter.PhotoImage(file=filename)
        copy_file(filename, 'images/src.png')
        canvas1.create_image(200, 200, image=image_src)
        lb.config(text="您选择的文件是：" + filename)
    else:
        lb.config(text="您没有选择任何文件")


# 开始识别函数
def now(select_back):
    show_result.delete(0, tkinter.END)
    _auto = lambda: messagebox.askyesno('auto', '是否自动截图? 取消则为手动截图')
    ask_auto = _auto()
    if not ask_auto:
        hand_number.main_hand()
    filename = r'C:\Users\10583\Desktop\ML_num\images\text.png'
    # 询问真值
    real_num = lambda: askinteger("真实值?", "请输入真实值")
    rn = real_num()
    while not rn:
        if rn == 0:
            break
        error = lambda: messagebox.askyesno('错误', '未输入真实值, 是否重新输入')
        E = error()
        if E:
            rn = real_num()
        else:
            return
    if not ask_auto:
        zero_one.save_pic_to_file('{}_{}'.format(str(rn), get_next_num.file_dir(rn)), mode=0)
    else:
        zero_one.save_pic_to_file('{}_{}'.format(str(rn), get_next_num.file_dir(rn)), path='images/src.png', mode=1)
    # 显示灰度图
    global image_text
    image_text = tkinter.PhotoImage(file=filename)
    canvas2.create_image(200, 200, image=image_text)
    # print(select_back.get(), type(select_back.get()))
    test_num, error_sum, mistake_num, total_time, result_list, testFileList = kNN.main(trained=select_back.get())
    show_result.insert(0,
                       "测试集总数为:" + test_num + ' ' + '测试出错总数:' + error_sum + ' ' + '错误率:' + mistake_num + ' ' + '耗 时 = ' + total_time)
    for i in range(1, len(result_list) + 1):
        show_result.insert(i, result_list[i - 1] + ' 文件名: ' + testFileList[i - 1])


def openword():
    webbrowser.open('readme.doc')


# 查看文件
def see():
    show_result.delete(0, tkinter.END)
    dir_list = os.listdir('testDigits/')
    for i in range(len(dir_list)):
        show_result.insert(i, dir_list[i])


# testDigits操作
def testDigit():
    op_test = tkinter.Toplevel(root)
    op_test.geometry('500x370')
    op_test.resizable(False, False)
    op_test.title('操作testDigit')
    scro = tkinter.Scrollbar(op_test)
    scro.place(x=475, y=10, height=300, width=15)
    show_file = tkinter.Listbox(op_test, yscrollcommand=scro.set)
    show_file.place(x=10, y=10, height=300, width=465)
    scro.config(command=show_file.yview)
    dir_list = os.listdir('testDigits/')
    for i in range(len(dir_list)):
        show_file.insert(i, dir_list[i])

    def del_file():
        selection = show_file.curselection()
        if not selection:
            tkinter.messagebox.showinfo(title='Information', message='No Selection')
        else:
            # print(selection, 'get: ',show_file.get(selection))
            os.remove('testDigits/{}'.format(show_file.get(selection)))
            show_file.delete(selection)

    def add_training():
        selection = show_file.curselection()
        if not selection:
            tkinter.messagebox.showinfo(title='Information', message='No Selection')
        else:
            num = show_file.get(selection)
            copy_file('testDigits/{}'.format(num),
                      "trainingDigits/{}_{}.txt".format(num[0], get_next_num.file_dir(num[0], 'trainingDigits/') - 1))
            show_file.delete(selection)

    del_button = Button(op_test, text='删除', command=del_file)
    add_button = Button(op_test, text='添加到训练集', command=add_training)
    del_button.place(x=10, y=320, height=40, width=200)
    add_button.place(x=290, y=320, height=40, width=200)


# 测试正确率
def get_num():
    show_result.delete(0, tkinter.END)
    check_TestDigit = messagebox.askyesno('查看正确率或测试集识别结果', '是否查看正确率')
    if check_TestDigit:
        test_num, error_sum, mistake_num, total_time, result_list, testFileList = check.check()
    else:
        try:
            test_num, error_sum, mistake_num, total_time, result_list, testFileList = kNN.main()
        except ZeroDivisionError:
            e = lambda: messagebox.showinfo('测试集错误', '没有测试集')
            e()
            return
    show_result.insert(0,
                       "测试集总数为:" + test_num + ' ' + '测试出错总数:' + error_sum + ' ' + '错误率:' + mistake_num + ' ' + '耗 时 = ' + total_time)
    for i in range(1, len(result_list) + 1):
        show_result.insert(i, result_list[i - 1] + ' 文件名: ' + testFileList[i - 1])


lb = Label(root, text='你可以点击 ABOUT->Help 查看帮助文档')
lb.pack()
select_file = Button(root, text="选择文件", command=Open)
select_file.place(x=10, y=20, height=40, width=200)

cama = Button(root, text='摄像头', command=vedio_cut.get_img_from_camera_local)
cama.place(x=220, y=20, height=40, width=200)
result = Button(root, text='开始识别', command=lambda: now(select_back))
result.place(x=430, y=20, height=40, width=200)
label_back = tkinter.Label(root, text='使用备份:')
label_back.place(x=640, y=30, height=20)
# 1为使用, 0为不使用
select_back = tkinter.IntVar()
select_back.set(1)
radioBack = tkinter.Radiobutton(root, variable=select_back, value=1, text='是')
radioBack.place(x=700, y=30, width=40, height=20)
radioNew = tkinter.Radiobutton(root, variable=select_back, value=0, text='否')
radioNew.place(x=745, y=30, width=40, height=20)

# 画板
# 创建画布
showimage1 = tkinter.PhotoImage()
canvas1 = tkinter.Canvas(root, bg='white', width=400, height=400)
canvas1.place(x=10, y=80)

showimage2 = tkinter.PhotoImage()
canvas2 = tkinter.Canvas(root, bg='white', width=400, height=400)
# canvas2.create_image(400, 400, image=showimage2)
canvas2.place(x=420, y=80)

# 创建列表框组件和滚动条
scroll = tkinter.Scrollbar(root)
scroll.place(x=810, y=500, width=15, height=200)
show_result = tkinter.Listbox(root, width=300, yscrollcommand=scroll.set)
show_result.place(x=10, y=500, width=800, height=200)
scroll.config(command=show_result.yview)
# show_result.insert(0, result)

# 创建菜单
menu = tkinter.Menu(root)
# 数据操作
submenu = tkinter.Menu(menu, tearoff=0)
submenu.add_command(label='SEE', command=see)
submenu.add_command(label='testDigit', command=testDigit)
# submenu.add_command(label='DELETE_image', command=None)
menu.add_cascade(label='Digit', menu=submenu)

# About
submenu = tkinter.Menu(menu, tearoff=0)
submenu.add_command(label='ABOUT ME', command=lambda: messagebox.showinfo(title='关于我', message='kNN'))
submenu.add_command(label='Help', command=openword)
submenu.add_command(label='CHECK', command=get_num)
menu.add_cascade(label='ABOUT', menu=submenu)
root.config(menu=menu)

if __name__ == '__main__':
    root.mainloop()
