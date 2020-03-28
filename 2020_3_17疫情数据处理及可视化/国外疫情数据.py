import requests
import re
import json
import os
import csv
from pyecharts import Map


def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
    response = requests.get(url=url, headers=headers, timeout=10)
    response.encoding = response.apparent_encoding
    # pprint.pprint(response.text)
    selects = re.findall('try \{ window.getListByCountryTypeService2true =(.*?)\}catch\(e\)\{\}', response.text, re.S)
    results = json.loads(selects[0])

    path = '国外疫情数据'
    if not os.path.exists(path):
        os.mkdir(path)

    # 亚洲Asia    非洲Africa    南美洲South_America     北美洲North_America   非洲Africa  大洋洲Oceania   欧洲Europe
    areas = ['亚洲', '非洲', '南美洲', '北美洲', '非洲', '大洋洲', '欧洲']
    for area in areas:
        f = open(path + '/' + '{}国家疫情数据.csv'.format(area), mode="w", newline="", encoding="utf-8-sig")
        csv_write = csv.writer(f)
        csv_write.writerow(['国家中文名称', '国家英文名称', '现存确诊', '累计确诊', '治愈', '死亡'])
        f.close()
    values = []             # 存储现存确诊人数超过1000的国家的准确数值
    attrs = []
    for result in results:
        continents = result['continents']  # 代表所在的洲
        provinceName = result['provinceName']  # 代表国家中文名称
        countryFullName = result['countryFullName']  # 代表国家英文名称
        currentConfirmedCount = result['currentConfirmedCount']  # 现存确诊
        confirmedCount = result['confirmedCount']  # 累计确诊
        curedCount = result['curedCount']  # 治愈
        deadCount = result['deadCount']  # 死亡
        attrs.append(result['countryFullName'])
        values.append(int(currentConfirmedCount))


        if continents in areas:
            f = open(path + '/' + '{}国家疫情数据.csv'.format(continents), mode="a+", newline="", encoding="utf-8-sig")
            csv_write = csv.writer(f)
            csv_write.writerow(
                [provinceName, countryFullName, currentConfirmedCount, confirmedCount, curedCount, deadCount])
            f.close()
    paint_map(values,attrs)

def paint_map(values,attrs):
    map0 = Map('世界疫情重度国家分布图',width=1200,height=600)
    map0.add('世界地图',attrs,values, maptype="world",  is_visualmap=True, visual_text_color='#000')
    map0.render(path="./国外疫情数据/世界疫情重度国家分布图.html")
    


if __name__ == '__main__':
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0'
    get_url(url)