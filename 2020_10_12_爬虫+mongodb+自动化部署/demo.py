import requests
import os
import datetime
import csv
import xml.dom.minidom
import pymongo
import time

def main():
    path = "datas"
    # 不存在当前目录则创建一个此目录
    if not os.path.exists(path):
        os.mkdir(path)
    # 获取当前日期
    time_now = str(datetime.datetime.now()).split(' ')[0].split('-')
    year = time_now[0]
    month = time_now[1]
    day = int(time_now[2])-1
    # 返回需要的参数
    return path,year,month,day


def get_real_url():
    path,year,month,day = main()
    # 每天创建新的文件夹（以日期命名）
    path_now = path + '/' + '{}-{}-{}'.format(year,month,day)
    if not os.path.exists(path_now):
        os.mkdir(path_now)
    url = 'http://www.cffex.com.cn/sj/ccpm/{}{}/{}/IF.xml?id'.format(year,month,day)
    response = requests.get(url=url)
    # 实现万能解码
    response.encoding = response.apparent_encoding
    html = response.text
    # 返回需要的数据
    return html,path_now


def download_data():
    html,path = get_real_url()
    with open(path + '/' + 'data.xml',mode='w',encoding='utf-8') as f:
        f.write(html)
    f.close()
    return path


def save_to_csv():
    path = download_data()
    # 打开xml文档
    dom = xml.dom.minidom.parse(path + '/' + 'data.xml')
    # 得到文档元素对象
    root = dom.documentElement
    instrumentids = dom.getElementsByTagName("instrumentid")
    ranks = dom.getElementsByTagName("rank")
    names = dom.getElementsByTagName("shortname")
    volumes = dom.getElementsByTagName("volume")
    varvolumes = dom.getElementsByTagName("varvolume")
    # 合约有IF2012、IF2011、IF2010、IF2103
    strings = ['IF2012','IF2011','IF2010','IF2103']
    for s in strings:
        f = open(path + '/' + '{}.csv'.format(s),newline="",encoding='utf-8-sig',mode='w')
        csv_write = csv.writer(f)
        csv_write.writerow(['名次','会员简称','持买单量','比上交易日增减'])
    for i in range(len(names)):
        id = instrumentids[i].firstChild.data
        name = names[i].firstChild.data
        rank = ranks[i].firstChild.data
        volume = volumes[i].firstChild.data
        varvolume = varvolumes[i].firstChild.data
        if id == 'IF2012':
            f = open(path + '/' + '{}.csv'.format(id),newline="",encoding='utf-8-sig',mode='a+')
            csv_write = csv.writer(f)
            csv_write.writerow([rank, name,volume, varvolume])
        elif id == "IF2011":
            f = open(path + '/' + '{}.csv'.format(id), newline="", encoding='utf-8-sig', mode='a+')
            csv_write = csv.writer(f)
            csv_write.writerow([rank, name,volume, varvolume])
        elif id == "IF2010":
            f = open(path + '/' + '{}.csv'.format(id), newline="", encoding='utf-8-sig', mode='a+')
            csv_write = csv.writer(f)
            csv_write.writerow([rank, name,volume, varvolume])
        elif id == "IF2103":
            f = open(path + '/' + '{}.csv'.format(id), newline="", encoding='utf-8-sig', mode='a+')
            csv_write = csv.writer(f)
            csv_write.writerow([rank, name,volume, varvolume])
    return path

def save_data_to_mongodb():
    # 连接本地mongodb数据库
    myclient = pymongo.MongoClient(host='127.0.0.1', port=27017)
    # 若不存在，则创建mydb数据库
    path, year, month, day = main()
    mydb = myclient["{}-{}-{}".format(year,month,day)]
    strings = ['IF2012','IF2011','IF2010','IF2103']
    path = save_to_csv()
    # 依次创建数据表
    for string in strings:
        mycol = mydb[string]
        f = open(path + '/' + '{}.csv'.format(string),mode='r',encoding='utf-8')
        csv_reader = csv.reader(f)
        rows = [i for i in csv_reader]
        datas = []
        for i in range(1,len(rows)):
            data = {}
            data[rows[0][0]] = rows[i][0]
            data[rows[0][1]] = rows[i][1]
            data[rows[0][2]] = rows[i][2]
            data[rows[0][3]] = rows[i][3]
            datas.append(data)
        mycol.insert_many(datas)
    print('{}/{}/{}中金所数据爬取并写入到mongodb数据库'.format(year,month,day))




if __name__ == '__main__':
    save_data_to_mongodb()
