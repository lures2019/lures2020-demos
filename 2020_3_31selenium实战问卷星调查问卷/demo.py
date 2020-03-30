from selenium import webdriver
import random
import time

def start_times():
    url = 'https://www.wjx.cn/jq/68355437.aspx'
    drive = webdriver.Chrome()  # 开启web浏览器的Chrome驱动
    drive.get(url)  # 使用电脑浏览器启动此问卷

    elements = drive.find_elements_by_css_selector('.div_question')

    multiple_choices = [0, 1, 2, 3, 5, 7, 8, 10, 11, 14, 15, 16, 17, 18]  # 单选题
    multiple_choice_questions = [4, 6, 9, 12, 13]  # 多选题
    subjective_questions = [19]  # 主观题

    # 先来填写单选题
    for i in (multiple_choices):
        answer = elements[i]
        lis = answer.find_elements_by_css_selector('li')
        lis[random.randint(0, len(lis) - 1)].click()

    # 填写多选题
    for j in multiple_choice_questions:
        answer = elements[j]
        lis = answer.find_elements_by_css_selector('li')
        length = len(lis)
        l = [i for i in range(length)]
        l = random.choices(l, k=min(int(length / 2), 3))  # random.choice()打乱顺序
        for i in l:
            lis[i].click()

    # 填写主观题
    lis = drive.find_elements_by_css_selector('#q20')[0]
    lis.clear()
    sayings = ['很好', '没有建议', '你看着办吧！', '我喜欢耐克！', '我喜欢lures！', '哈哈哈，终于完成了']
    i = random.randint(0, len(sayings)-1)
    lis.send_keys(sayings[i])

    # 提交问卷
    click_button = drive.find_element_by_css_selector('.submitbutton')
    click_button.click()
    time.sleep(3)
    drive.quit()


if __name__ == '__main__':
    for i in range(10):
        start_times()
        print("第{}次刷单!".format(i+1))