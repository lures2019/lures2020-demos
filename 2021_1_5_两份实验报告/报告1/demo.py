from tkinter import *
from tkinter import messagebox
import requests


"""搭建界面"""
def translation():
    """完成翻译的功能"""
    """
        1、获取用户的输入
        2、通过爬取【百度翻译、谷歌翻译或者有道翻译】翻译结果
        3、根据获取的结果，显示到窗口上
    """
    # 获取用户输入的结果
    content = entry.get()
    # 去除多余的空格，用于判断用户手输入了信息！
    con = content.strip()
    if con == "":
        messagebox.showinfo('提示', '请输入要翻译的内容!')
    else:
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=1972418272@10.108.160.105; JSESSIONID=aaaXYvTD-n_jObqhJjGex; OUTFOX_SEARCH_USER_ID_NCOO=846912277.6744791; ___rl__test__cookies=1585383917099',
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        """
            注意：url网址本来是"http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
                 但是在data中存在的几个参数涉及到js解密，时间戳的问题
                 所以这里一个取巧的方式就是把网址中的_o去掉(虽然不知道原因)
        """
        data = {
            'i': con,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        response = requests.post(url=url,headers=headers,data=data)
        response.encoding = response.apparent_encoding
        res = response.json()['translateResult'][0][0]['tgt']
        # 将结果显示到窗口上
        result.set(res)
        return res


# 创建窗口
window = Tk()
# 窗口的大小,前两个参数是：宽、高，后面的参数是坐标
window.geometry('335x100+800+400')
# 禁止窗口的拉伸
window.resizable(0, 0)
# 窗口的标题
window.title("中英互译器")

# 控件
label = Label(window, text="请输入要翻译的文字：", font=("仿宋", 12))
# 位置，网格式的布局
label.grid(row=0, column=0, sticky='e')
# 输入框
entry = Entry(window, font=("仿宋", 12))
# row和column的作用：该表label控件的位置
entry.grid(row=0, column=1)

label1 = Label(window, text="翻译之后得到的文字：", font=("仿宋", 12))
# sticky是实现对齐方式的
label1.grid(row=1, column=0, sticky='e')

# 随时变化的量
result = StringVar()
entry1 = Entry(window, font=("仿宋", 12),textvariable=result)
entry1.grid(row=1, column=1)

# 空出一行,使布局漂亮些
label2 = Label(window, text="")
label2.grid(row=2, column=0)

# 按钮
# command = translation完成事件的绑定
button = Button(window, text="翻译", width="10", command=translation)
button.grid(row=3, column=0, sticky='w')
# command = window.quit是用来退出界面的！
button1 = Button(window, text="退出", width="10", command=window.quit)
button1.grid(row=3, column=1, sticky='e')

# 显示窗口(消息循环)
window.mainloop()
