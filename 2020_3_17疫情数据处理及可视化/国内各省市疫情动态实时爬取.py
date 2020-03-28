import requests
import re
import json
import os
import csv
from pyecharts import Map



def get_url(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding
        selects = re.findall('try \{ window.getAreaStat =(.*?)\}catch\(e\)\{\}', response.text, re.S)
        results = json.loads(selects[0])
        path = '国内今日数据'
        # 不存在此目录则创建此目录
        if not os.path.exists(path):
                os.mkdir(path)
        f = open(path + '/' + '国内各省市今日数据.csv', mode="w", newline="", encoding="utf-8-sig")
        csv_write = csv.writer(f)
        csv_write.writerow(['省份名称', '省份简称或者是直辖市', '现存确诊', '累计确诊', '死亡', '治愈'])

        attrs = []  # 存储中国各省、自治区
        values = []  # 存储各省现存确诊数

        hubei_values = []       # 存储湖北各市现存确诊数
        hubei_attrs = []        # 存储湖北省各地级市
        for result in results:
                provinceName = result['provinceName']  # 省份名称
                provinceShortName = result['provinceShortName']  # 省份简称
                currentConfirmedCount = result['currentConfirmedCount']  # 现存确诊
                confirmedCount = result['confirmedCount']  # 累计确诊
                curedCount = result['curedCount']  # 治愈
                deadCount = result['deadCount']  # 死亡
                cities = result['cities']  # 当前省下的地级市或自治区
                csv_write.writerow([provinceName, provinceShortName, currentConfirmedCount, confirmedCount, curedCount, deadCount])
                if len(cities) != 0:
                        for city in cities:
                                cityName = city['cityName']  # 存储地级市名称
                                currentConfirmedCount1 = city['currentConfirmedCount']  # 现存确诊
                                confirmedCount1 = city['confirmedCount']  # 累计确诊
                                curedCount1 = city['curedCount']  # 治愈
                                deadCount1 = city['deadCount']  # 死亡
                                csv_write.writerow(['', cityName, currentConfirmedCount1, confirmedCount1, curedCount1,deadCount1])
                                if provinceShortName == '湖北':
                                        if cityName != '神农架林区':
                                                hubei_attrs.append(cityName + '市')
                                        else:
                                                hubei_attrs.append(cityName)
                                        hubei_values.append(currentConfirmedCount1)
                                else:
                                        pass
                else:
                        pass
                attrs.append(provinceShortName)
                values.append(currentConfirmedCount)
        paint_map_china(values,attrs)
        paint_map_hubei(hubei_values,hubei_attrs)

def paint_map_china(values,attrs):
        map0 = Map('中国各省疫情分布图', width=1200, height=600)
        map0.add('中国地图', attrs, values, maptype="china",visual_range=[0, 100], is_visualmap=True, visual_text_color='#000')
        map0.render(path='./国内今日数据/各省疫情分布图分布图.html')

def paint_map_hubei(hubei_values,hubei_attrs):
        path = '湖北今日数据'
        if not os.path.exists(path):
                os.mkdir(path)
        map0 = Map("湖北疫情分布图",'湖北',width=1200,height=600)
        map0.add("湖北",hubei_attrs,hubei_values,maptype="湖北",visual_range=[0,500],is_visualmap=True,visual_text_color="#000")
        map0.render(path + '/' + '湖北各市疫情分布图.html')

if __name__ == '__main__':
        url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0'
        get_url(url)