from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import csv

# 封装函数，传url以及path
def get_course_messages(url,path,pages):
    # executable_path为chromedriver.exe的解压安装目录，需要与python解释器同一文件夹下
    driver = webdriver.Chrome(executable_path="D:/python/chromedriver.exe")
    url = url
    driver.get(url)
    # 获得初始页面代码，接下来进行简单的解析
    cont = driver.page_source
    soup = BeautifulSoup(cont, 'html.parser')
    # 模仿浏览器就行点击查看课程评价的功能
    ele = driver.find_element_by_id("review-tag-button")
    # 上边的id，下边的classname都可以在源码中看到（首选火狐，谷歌）
    ele.click()
    # 翻页功能，类名不能有空格，有空格可取后边的部分
    xyy = driver.find_element_by_class_name("ux-pager_btn__next")
    connt = driver.page_source
    soup = BeautifulSoup(connt, 'html.parser')
    # n页的总评论
    acontent = []
    # 包含全部评论项目的总表标签
    content = soup.find_all('div', {'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'})
    # 第一页评论的爬取
    page_message = []
    for ctt in content:
        scontent = []
        # 刚获得一页中的content中每一项评论还有少量标签
        aspan = ctt.find_all('span')
        for span in aspan:
            # 只要span标签里边的评论内容
            scontent.append(span.string)
            # 将一页中的所有评论加到总评论列表里，直到该页加完
        page_message.append(scontent)
    acontent.append(page_message)
    # 翻页
    for i in range(1,pages):
        xyy.click()
        connt = driver.page_source
        soup = BeautifulSoup(connt, 'html.parser')
        # 包含全部评论项目的总表标签
        content = soup.find_all('div', {'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'})
        page_message_now = []
        for ctt in content:
            scontent = []
            aspan = ctt.find_all('span')
            for span in aspan:
                scontent.append(span.string)
            page_message_now.append(scontent)
        acontent.append(page_message_now)
    # 创建对应的csv文件
    f = open(path + '/' + '课程评价.csv',mode="a+",encoding='utf-8-sig',newline="")
    csv_write = csv.writer(f)
    for i in range(len(acontent)):
        for j in range(len(acontent[i])):
            csv_write.writerow(acontent[i][j])


if __name__== '__main__':
    urls = ['https://www.icourse163.org/course/HACTCM-1205683805','https://www.icourse163.org/course/WHU-1001717005'
            ,'https://www.icourse163.org/course/NJU-1002190001','https://www.icourse163.org/course/XJTU-1003367021']
    paths = ['中国医学史','思想道德修养与法律基础','中华优秀传统文化','医学人文']
    # 创建对应的文件夹
    for path in paths:
        # 不存在则创建此目录
        if not os.path.exists(path):
            os.mkdir(path)
    # 分别查看四门课程评论的页数
    pages = [10,245,98,6]
    for i in range(len(paths)):
        get_course_messages(urls[i],paths[i],pages[i])
        # 设置10s的休眠时间
        time.sleep(10)
        print("{}课程评价爬取完毕！".format(paths[i]))

