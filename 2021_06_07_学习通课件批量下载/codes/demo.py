"""
    author:lures
    date:2021/06/07
    title:批量下载学习通课件
"""

import requests
import parsel
import os
from selenium import webdriver
import time
from pykeyboard import PyKeyboard


# 经过删除后的最简url
"""
    courseId后面的数字明显是课程的编号id
    classId后面的数字是班级的编号id
    enc后面的字符串估计是cookie信息，删除重新加载就会打不开页面
    
    前两项可以根据自己的需要进行修改，后面的cookie状态需要自己登录验证(可以在网页的Query String Parameters得到验证)
"""
url = 'http://mooc1.xueyinonline.com/coursedata?'
# 这边建议使用这种方式写，直接写url的时候可能会加载出登录页面
param = {
    'courseId': '216843891',
    'classId': '37442199',
    'enc': '4e201cc7ccb3a77d732764aae2ad1593'
}
# 习惯加上必要的请求头————应对反爬虫最基础手段
headers = {
    'Cookie': 'lv=4; fid=42845; 42845userinfo=2f53fd8af056f0119dcd337c66f6e822d807a544f7930b6abeaaa6286f1f17540218b49dee77ef73c98bf515e9147871159686b24a339510e7fafd565af53bf2; 42845UID=77635629; 42845enc=C84513F365AD986B0E3FB9420464EB70; _uid=77635629; uf=d9387224d3a6095b0913d0d1304e4d0e1c322d17a756323c68a9d3691f5c58ea2d6715939c5a4b6a06f4cac8ed4e1fdf913b662843f1f4ad6d92e371d7fdf644c350fd0277492a5e31debf8b297bbc625558ebfe920d455c9c3c1e0ea03367440766c3fef1ce0139; _d=1622790254538; UID=77635629; vc=C84513F365AD986B0E3FB9420464EB70; vc2=6AF50A892AB7037304058361D74D96A4; vc3=daaplFzxvsvw%2FIg8LC1kShx%2FcIrpdaX2lvWt9L1pEoZEZcp68rSGEppB9DGAXNz8Simy9diGDgHHAegiSp9ZJadEfEvcl%2B0n3%2F%2BudNVMzXK1sCQtuCjnDEkRybXlFxWjWqeaO8MbTk8N4WBwQ3BuIIbGBwVSqnkDLKRn75BO%2Fsg%3D1af16cdb346171a098be5c4ae07c5bae; xxtenc=1ccbb8b204a6a78f71853e7e707897ca; DSSTASH_LOG=C_38-UN_3837-US_77635629-T_1622790254539; k8s=2c41682606984fafbf33c9132344b9d7768d09f4; route=bca6486eee9aca907e6257b7921729c3; jrose=32614F47D5A9F7E3A600459C4B55D2C3.mooc-2190841352-5lxm4',
    'Host': 'mooc1.xueyinonline.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
response = requests.get(url,params=param,headers=headers)
response.encoding = response.apparent_encoding
select = parsel.Selector(response.text)
# 找到文件夹的名称
find_folder_names = select.xpath('//tbody[@id="tableId02"]/tr/td[@align="left"]/div[2]/a/text()').getall()
# 找到对应文件夹下的打开链接
folder_url = 'http://mooc1.xueyinonline.com/coursedata?'
folder_id = select.xpath('//tbody[@id="tableId02"]/tr/@id').getall()
# 开始创建对应的文件夹
for i in range(len(find_folder_names)):
    # 不存在此目录则创建一个
    path = find_folder_names[i]
    if not os.path.exists(path):
        os.mkdir(path)
    # 注意每一个文件夹对应的dataId、dataName都是不一样的
    folder_param = {
        'courseId': '216843891',
        'dataName': find_folder_names[i],
        'dataId': folder_id[i],
        'classId': '37442199',
        'enc': '4e201cc7ccb3a77d732764aae2ad1593'
    }
    # 进行请求
    new_response = requests.get(folder_url,params=folder_param,headers=headers)
    new_response.encoding = new_response.apparent_encoding
    # 开始提取所有课件链接
    select_new = parsel.Selector(new_response.text)
    # 对于只有一层目录的可以直接保存，还有一层目录的，还要进行同样操作
    hrefs = select_new.xpath('//tbody[@id="tableId02"]/tr/td[2]/div[1]/a[1]/@href').getall()
    if len(hrefs) != 0:
        # 获取文件的名称以及格式
        name = select_new.xpath('//tbody[@id="tableId02"]/tr/td[2]/div[2]/a/@name').getall()
        # 开始保存文件
        for i in range(1):
            end_url = 'http://mooc1.xueyinonline.com' + hrefs[i]
            # 不能直接使用链接下载，所以使用selenium自动化点击
            print(end_url)
            driver = webdriver.Chrome()
            time.sleep(2)
            driver.get(end_url)
            # 窗口全屏
            driver.maximize_window()
            # 定位到密码和用户栏，填入信息
            number_input_box = driver.find_element_by_id('phone')
            # 在XXXXXXXXXX处改为自己的手机号和密码
            try:
                number_input_box.send_keys('XXXXXXXXXXX')
            except Exception as error:
                print("selenium定位失败")
            password_input_box = driver.find_element_by_id('pwd')
            try:
                password_input_box.send_keys('XXXXXXXXXXX')
            except Exception as error:
                print("selenium定位失败")
            button = driver.find_element_by_id('loginBtn')
            try:
                button.click()
            except Exception as e:
                print("selenium点击按钮失败")

            """关于针对Windows下载弹窗的处理 """
            # https://blog.csdn.net/qq_34659777/article/details/103807535
            k = PyKeyboard()
            # 更换下载目录,先按9次tab键更改路径
            for i in range(5):
                k.press_key(k.tab_key)
                k.release_key(k.tab_key)
                time.sleep(1)
            k.tap_key(k.tab_key)
            k.tap_key(k.enter_key)
            time.sleep(1)
            for i in range(4):
                k.press_key(k.tab_key)
                k.release_key(k.tab_key)
                time.sleep(1)
            # 开始键入文件夹名称，切换英文状态
            k.tap_key(k.backspace_key)
            time.sleep(1)
            k.tap_key(k.shift_key)
            time.sleep(1)
            k.type_string('D:/lures2020-demos/2021_06_07_学习通课件批量下载/codes/{}'.format(path))
            time.sleep(1)
            # 按回车键
            k.tap_key(k.enter_key)
            time.sleep(1)
            for i in range(7):
                k.press_key(k.tab_key)
                k.release_key(k.tab_key)
                time.sleep(1)
            k.tap_key(k.enter_key)
            time.sleep(1)
            for i in range(3):
                k.press_key(k.tab_key)
                k.release_key(k.tab_key)
                time.sleep(1)
            # 开始按回车键,会下载临时文件，但还要按保存
            # 模拟Tab,否则不会保存成功
            # 发送Enter回车
            k.tap_key(k.enter_key)
            print("》》》》》》》》{}下载完毕！《《《《《《《《".format(name[i]))
    else:
        pass