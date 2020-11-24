import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"在头部标签里找到并输入","Cookie":"在头部标签里找到并输入"}

url = "输入url网址"
r = requests.get(url,headers=headers)
c = r.status_code
if c ==200:
    r.encoding = 'UTF-8'
    Test = r.text
    soup = BeautifulSoup(Test,'html.parser')
    tiebaliuyan = soup.find_all(attrs={'class':'p_postlist'})[0].text
    with open ('贴吧留言.txt',mode = 'a',encoding = 'utf-8')as f:
         f.write(str(tiebaliuyan))
         f.write('\n')
         f.close

else:print('c')
