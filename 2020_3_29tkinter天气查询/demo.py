from tkinter import *
from tkinter import messagebox
import requests
import parsel


def get_cookie(url):
    cookie = requests.get(url=url, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }, allow_redirects=False).cookies
    return cookie

def get_now_weather():
    content = entry.get()
    # 去除用户不必要的空格
    con = content.strip()
    if con == "":
        messagebox.showinfo("提示", "请输入要查询的城市的拼音！")
    else:
        try:
            url = 'https://m.tianqi.com/' + con
            headers = {
                'cookie': 'cityPy=jinan; cityPy_expire=1586050179; Hm_lvt_b6bbdb7cf5398f3880daf0f6cd1e05db=1585445380; UM_distinctid=17123e8a083410-03c3ccb4de3e4e-376b4502-ff000-17123e8a08435a; CNZZDATA1259910480=1975027729-1585444105-%7C1585444105; CNZZDATA1277676127=1109901115-1585444275-%7C1585444275; PHPSESSID=sfn8md5h574bc0ad72hqre2ln5; Hm_lpvt_b6bbdb7cf5398f3880daf0f6cd1e05db=1585445438',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }
            response = requests.get(url=url, headers=headers, cookies=get_cookie(url))
            response.encoding = response.apparent_encoding
            select = parsel.Selector(response.text)
            weather = []
            weather.append(str(select.xpath('//dl[@class="temp"]/dd[@class="now"]/text()').get()) + '°C')
            message = select.xpath('//dl[@class="temp"]/dd[@class="txt"]/text()').get()
            datalist = ['多云', '晴', '小雨', '阴', '中雨']
            logo = []
            for data in datalist:
                if data in message:
                    logo.append(data)
            weather.append(message)
            weather.append(select.xpath('//div[@class="info"]/a[@class="b1"]/text()').get())
            weather.append(select.xpath('//div[@class="info"]/span[@class="b2"]/text()').get())
            weather.append(select.xpath('//div[@class="info"]/span[@class="b3"]/text()').get())
            result.set(weather)
        except Exception as error:
            messagebox.showinfo("警告","没有该位置的天气信息！")

window = Tk()
window.geometry("654x100+600+400")
window.resizable(0, 0)
window.title("天气预报")

# 控件
label = Label(window, text="请输入您想查询的城市的拼音：", font=("仿宋", 12))
label.grid(row=0, column=0, sticky=W)
entry = Entry(window, font=("仿宋", 12),width="52")
entry.grid(row=0, column=1)

label1 = Label(window, text="查询到的当前天气情况：", font=("仿宋", 12))
label1.grid(row=1, column=0, sticky=W)
result = StringVar()
entry1 = Entry(window, font=("仿宋", 12),textvariable=result,width="52")
entry1.grid(row=1, column=1)

label2 = Label(window,text="")
label2.grid(row=2, column=0)

# 按钮
button = Button(window, text="查询当前天气", font=("仿宋", 12), width="12", command=get_now_weather)
button.grid(row=3, column=0, sticky=W)
button1 = Button(window, text="退出", font=("仿宋", 12), width="10",command=window.quit)
button1.grid(row=3, column=1, sticky=E)

window.mainloop()