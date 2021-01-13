import requests
from bs4 import BeautifulSoup


def question1_to_3():
    url = 'https://www.ryjiaoyu.com/'
    response = requests.get(url)
    # 打印出响应对应的连接状态码
    print(response.status_code)
    # 打印出人民邮电出版社网站首页编码
    print(response.encoding)
    # 打印出人民邮电出版社网站首页响应对象的响应头信息
    print(response.headers)

    # 使用bs4提取导航栏
    soup = BeautifulSoup(response.text, 'html.parser')
    head_navs = soup.find(name='ul', attrs={"class": "head-nav"}).get_text()
    # 创建列表，接受信息并处理
    navs_end = []
    for i in head_navs:
        if len(i) == 0 or i == '\n' or i == ' ':
            pass
        else:
            navs_end.append(i)
    # navs就是最后的列表
    navs = [navs_end[i] + navs_end[i + 1] for i in range(0, 10, 2)]
    print(navs)

def question4(i):
    url = 'https://www.ryjiaoyu.com/search?q=python&page={}'.format(i)
    response = requests.get(url)
    # 使用bs4提取导航栏
    soup = BeautifulSoup(response.text, 'html.parser')
    # 创建列表，接受信息并处理
    book_titles = []
    for x in soup.find_all('a'):
        title = x.get('title')
        if title and "-" not in title:
            book_titles.append(title)
    return book_titles

if __name__ == '__main__':
    question1_to_3()
    # 书单列表
    books = []
    for i in range(5):
        books1 = question4(i)
        for book in books1:
            books.append(book)
    print(books)



