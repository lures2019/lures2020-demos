import csv
import requests


if __name__ == '__main__':
    # 创建测试地址数据集
    locationList = []
<<<<<<< HEAD
<<<<<<< HEAD
    f = open('深圳龙华房源信息.csv', mode='r', encoding='utf-8-sig')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    for row in rows:
        str_now = '深圳市' + row[1]
=======
=======
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
    f = open('上海嘉定房源信息.csv', mode='r', encoding='utf-8-sig')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    for row in rows[1:]:
        str_now = '上海市' + row[2] + row[3]
<<<<<<< HEAD
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
=======
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
        locationList.append(str_now)
    # 进行地理编码
    for i in range(len(locationList)):
        url = 'https://restapi.amap.com/v3/geocode/geo?address={}&output=json&key=84bb08664d7f042079e48b576d9dd7c1'.format(locationList[i])
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        data = response.json()['geocodes'][0]['location']
        if i == 0:
            rows[i].append("经度")
            rows[i].append("纬度")
        else:
            rows[i].append(data.split(',')[0])
            rows[i].append(data.split(',')[1])
<<<<<<< HEAD
<<<<<<< HEAD
        print(locationList[i])
=======
        print(i)
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
=======
        print(i)
>>>>>>> 286c01981047c181c0c2e16ef7c08630ff07151e
    fp = open('添加经纬度后csv文件.csv',mode='w',encoding='utf-8-sig',newline="")
    csv_write = csv.writer(fp)
    csv_write.writerow(rows[0])
    for row in rows[1:]:
        csv_write.writerow(row)
    fp.close()
