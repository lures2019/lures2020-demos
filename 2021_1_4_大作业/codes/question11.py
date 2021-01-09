"""
    爬取 食物营养成分 网站，得到相关数据
    网址类似如下：https://yingyang.bmcx.com/%E9%9D%A2__yingyang/
    要求：输入关键词可以获取到对应的数据保存到csv文件中
"""
import requests
import parsel
import os
import csv

# 爬取总体信息
def get_information(kd):
    url = 'https://yingyang.bmcx.com/{}__yingyang/'.format(kd)
    response = requests.get(url)
    # 万能解码
    response.encoding = response.apparent_encoding
    # 构造xpath提取规则
    select = parsel.Selector(response.text)
    key_words = select.xpath('//div[@id="main_content"]/ul[@class="list"]/li/a/text()').getall()
    hrefs = select.xpath('//div[@id="main_content"]/ul[@class="list"]/li/a/@href').getall()
    # 该链接列表不是完整的链接列表，需要加以构造
    real_links = ['https://yingyang.bmcx.com/' + i for i in hrefs]

    # 返回获取到的信息
    return real_links,key_words

# 爬取单独营养成分表
def get_nutrition(url,kd,link_dict):
    url = url
    keyword = kd
    link_dict = link_dict
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    select = parsel.Selector(response.text)
    # 元素名称，其实这个网站名称都是相同的
    # name1 = select.xpath('//div[@id="main_content"]/table/tr/th/a/text()').getall()
    # 元素的值
    value = select.xpath('//div[@id="main_content"]/table/tr/td/text()').getall()
    # 运算的单位
    # unit1 = select.xpath('//div[@id="main_content"]/table/tr/td/span/text()').getall()

    # 创建对应的csv文件
    name = link_dict[url]
    csv_write.writerow(["",name,value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],
                        value[10],value[11],value[12],value[13],value[14],value[15],value[16],value[17],value[18],value[19],value[20],
                        value[21],value[22],value[23]])


if __name__ == '__main__':
    # 用户输入关键词
    keywords = ['面条','馒头','油饼','稻米','糯米','玉米','小米','马铃薯','红薯','粉丝','黄豆','豆腐','豆浆',
                '腐竹','豆腐干','素什锦','豆沙','蚕豆','核桃','板栗','鲜花生','葵花子','西瓜子','白萝卜','胡萝卜','黄豆芽',
               '绿豆芽','茄子','番茄','辣椒','甜椒','冬瓜','黄瓜','苦瓜','南瓜','丝瓜','西葫芦','大蒜','洋葱','韭菜','大白菜',
               '小白菜','菜花','菠菜','芹菜茎','香菜','藕','芋头','姜','草菇','金针菇','平菇','木耳','香菇','海带','羊肉','鸡',
               '鸭','鹅','牛乳','酸奶','奶油','鸡蛋','鸭蛋','皮蛋','咸鸭蛋','鹌鹑蛋','草鱼','黄鳝','鲤鱼','鲫鱼','带鱼','对虾',
                '河蟹','鲍鱼','螺','鱿鱼','菜籽油','豆油','花生油','色拉油']
    # 使用utf-8-sig作用是解决中文乱码
    fp = open('所有食物分类以及网址信息.csv',mode='w',encoding='utf-8-sig',newline="")
    csv_write = csv.writer(fp)
    csv_write.writerow(['名称','网址'])
    # 存放所有链接
    urls = []
    for keyword in keywords:
        real_links, key_words = get_information(keyword)
        try:
            csv_write.writerow([key_words[0], real_links[0]])
        except Exception as error:
            print(error)
    fp.close()
    # 读取总文件，将网址和名称放入字典中进行匹配
    file = open("所有食物分类以及网址信息.csv", mode='r', encoding='utf-8')
    csv_reader = csv.reader(file)
    rows = [i for i in csv_reader]
    link_dict = {}
    for row in rows[1:]:
        if row[1] not in link_dict:
            link_dict[row[1]] = row[0]
            urls.append(row[1])
        else:
            pass
    with  open("所有食物相关信息整合.csv", mode='a+', encoding='utf-8-sig', newline="") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(["","食物名","能量/kcal","硫胺素/mg","钙/mg","蛋白质/g","核黄素/mg","镁/mg","脂肪/g","烟酸/mg","铁/mg",
                            "碳水化合物/g","维生素C/mg","锰/mg","膳食纤维/g","维生素E/mg","锌/mg","维生素A/微克","胆固醇/mg","铜/mg",
                            "胡萝卜素/微克","钾/mg","磷/mg","视黄醇当量/微克","钠/mg","硒/微克"])
        try:
            for i in range(len(keywords)):
                get_nutrition(urls[i],keywords[i],link_dict)
                print("{}总结完毕！".format(link_dict[urls[i]]))
        except Exception as error:
            print(error)
    f.close()