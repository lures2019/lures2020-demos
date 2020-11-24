"""
    一、怎么去寻找字体：
        1、像58、实习僧这些网站他们的字体是通过base64编码后放到网页中
        2、猫眼电影，是通过使用url加载字体文件
    二、特点：
        1、每次网络加载的字体文件的形状都不一样
        2、每次字体的code和name的形状都不一样
"""
import requests
import re
import base64
from fontTools.ttLib import TTFont
import parsel
import csv

def get_maoyan():
    url = 'http://piaofang.maoyan.com/rankings/year?year=2019&limit=100&tab=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    html = response.text
    # result中匹配到的是字体加密部分的数据
    result = re.search('charset=utf-8;base64,(.*?)\)',html).group(1)
    f = open('解密前.html','w',encoding='utf-8')
    f.write(html)
    return html,result

def analyse_font():
    html,font_face = get_maoyan()
    # 下面使用base64解密
    font_data = base64.b64decode(font_face)
    with open('maoyan.woff','wb') as f:
        f.write(font_data)
    # 将woff转化成Pycharm能看的xml格式,就可以看到里面的配置信息了code-->name-->shape
    base_font = TTFont('maoyan.woff')
    base_font.saveXML('maoyan.xml')
    # 1、找到code和name之间的映射关系
    # font.getBestCmap()可以返回code和name之间的关系,看到的code是10进制
    code_name_cmap = base_font.getBestCmap()
    # font['glyf']可以返回字体的所有形状，是一个字典对象
    base_name_glyf_map = base_font['glyf']
    # 根据id找,xml文件中id对应的name在不停的变化，所以需要从文件包导入
    lines = open('maoyan.xml','r').readlines()
    data_list = []
    for line in lines:
        rule = re.findall('<GlyphID id="(.*?)" name="(.*?)"/>',line)
        if(len(rule) != 0):
            data_list.append(rule)
    base_number_glyph_map = {}
    for i in range(len(data_list)):
        base_number_glyph_map[data_list[i][0][0]] = base_name_glyf_map[data_list[i][0][1]]
    """
        1、name-->code之间有一层映射关系
        2、name-->glyph之间有一层映射关系
        3、在网页中显示的是code
        4、只要找到glyph和真正的数字之间的关系，就能找到code和数字之间的关系
    """
    for code,name in code_name_cmap.items():
        # 十进制转化为十六进制
        # print(hex(code),name)
        # 2、name和glyph之间的映射关系
        current_glyph = base_name_glyf_map[name]
        # 怎么去对比两个字体是否相等
        for number,glyph in base_number_glyph_map.items():
            if glyph == current_glyph:
                # 只替换掉第一次出现的0
                code_now = str(hex(code)).replace("0","&#",1) + ';'
                print(code_now,number)
                html = re.sub(code_now.strip(),str(number),html)
                break
        with open('maoyan.html','w',encoding='utf-8') as f:
            f.write(html)
    return html

def first_page_spyder():
    # 爬取相关信息写入csv文件中
    html = analyse_font()
    select = parsel.Selector(html)
    # 分别是[电影名称、上映时间、票房(万元)、平均票价、场均人次]
    movie_titles = select.xpath('//div[@id="ranks-list"]/ul[@class="row"]/li[@class="col1"]/p[@class="first-line"]/text()').getall()
    movie_dates = select.xpath('//div[@id="ranks-list"]/ul[@class="row"]/li[@class="col1"]/p[@class="second-line"]/text()').getall()
    movie_moneys = select.xpath('//div[@id="ranks-list"]/ul[@class="row"]/li[@class="col2 tr"]/i[@class="cs"]/text()').getall()
    average_moneys = select.xpath('//div[@id="ranks-list"]/ul[@class="row"]/li[@class="col3 tr"]/i[@class="cs"]/text()').getall()
    movie_persons = select.xpath('//div[@id="ranks-list"]/ul[@class="row"]/li[@class="col4 tr"]/i[@class="cs"]/text()').getall()
    movie_links = select.xpath('//div[@id="ranks-list"]/ul[@class="row"]/@data-com').getall()
    links = []
    for movie_link in movie_links:
        link = 'http://piaofang.maoyan.com' + movie_link.replace("hrefTo,href:'",'').replace("'",'').strip()
        links.append(link)
    return movie_titles, movie_dates, movie_moneys, average_moneys, movie_persons, links

def save_data_to_csv():
    f = open('猫眼2019年电影信息.csv',mode="w",encoding='utf-8-sig',newline="")
    csv_write = csv.writer(f)
    csv_write.writerow(['电影名称','上映时间','票房(万元)','平均票价','场均人次','电影链接'])
    movie_titles, movie_dates, movie_moneys, average_moneys, movie_persons, links = first_page_spyder()
    for i in range(len(links)):
        csv_write.writerow([movie_titles[i],movie_dates[i],movie_moneys[i],average_moneys[i],movie_persons[i],links[i]])
    f.close()

if __name__ == '__main__':
    save_data_to_csv()