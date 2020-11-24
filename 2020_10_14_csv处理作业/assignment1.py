import csv

def analyse(path_to_file):
    path = path_to_file
    # Question1：计算至少一个条目的AQI PM2.5为100或更高的天数，每年用一行打印结果
    def question1(path):
        f = open(path, mode='r')
        csv_reader = csv.reader(f)
        # 使用csv模块，以列表的形式将数据进行存储
        rows = [i for i in csv_reader]

        # 可以看到AQI_PM2.5是在csv文件的第14列,Date是在16列
        """
        for i in range(len(rows[0])):
            if rows[0][i] == 'AQI_PM2.5':
                print(i)
        """
        # 构造一个字典，存放不同的年份空气指数为100及100以上的数量
        year_dict = {}
        for row in rows[1:]:
            day = row[16].replace(' ','-')
            # 只统计AQI_PM2.5不为空的那些数据
            if len(row[14]) > 0:
                # 只有不小于100的数据才统计
                if int(row[14]) >= 100:
                    # 去除同一天多项对结果造成的干扰
                    if day not in year_dict:
                        year_dict[day] = 1
        # 构造新字典，统计数据
        years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
        now_dict = {}
        # 字典中数据初始化为0
        for year in years:
            now_dict[year] = 0
        # 现在针对字典数据进行处理
        for key, value in year_dict.items():
            if len(key.split('-')[-1]) == 2:
                year = '20' + str(key.split('-')[-1])
                if year not in now_dict:
                    now_dict[year] = 1
                else:
                    now_dict[year] += 1
            else:
                year = str(key.split('-')[-1])
                if year not in now_dict:
                    now_dict[year] = 1
                else:
                    now_dict[year] += 1
        # 最后将每年的数据按照行打印出来
        for key, value in now_dict.items():
            if key in ['2014', '2015', '2018', '2020']:
                print('{}年有{}天，AQI PM2.5为100或更高'.format(key, value))
            else:
                print('{}年有{}天，AQI PM2.5等于或大于100'.format(key, value))

    # Question2：计算每个月中至少有一个等于或大于阈值读数的天数
    def question2(path):
        f = open(path, mode='r')
        csv_reader = csv.reader(f)
        rows = [i for i in csv_reader]
        # 第二问应该是根据  月-年构造字典
        # 因为一天可能有多次测量，容易对结果造成干扰，新建字典，加以解决
        day_dict = {}
        for row in rows[1:]:
            day = row[16].replace(' ','-')
            # 只统计AQI_PM2.5不为空的那些数据
            if len(row[14]) > 0:
                # 只有不小于33的数据才统计
                if int(row[14]) >= 33:
                    # 去除同一天多项对结果造成的干扰
                    if day not in day_dict:
                        day_dict[day] = 1
        # 下面构造新字典
        years = ['2015', '2016', '2017', '2018', '2019', '2020']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # 构造新字典now_dict
        now_dict = {}
        for year in years:
            for month in months:
                key = year + '-' + month
                if key not in now_dict:
                    now_dict[key] = 0
        # 现在开始统计前面的字典的数据
        for key, value in day_dict.items():
            if len(key.split('-')[-1]) == 2:
                year = '20' + key.split('-')[-1]
                month = str(key.split('-')[1][:3])
                key_now = year + '-' + month
                if key_now not in now_dict:
                    now_dict[key_now] = 1
                else:
                    now_dict[key_now] += 1
            else:
                year = key.split('-')[-1]
                month = str(key.split('-')[1][:3])
                key_now = year + '-' + month
                if key_now not in now_dict:
                    now_dict[key_now] = 1
                else:
                    now_dict[key_now] += 1

        # 重新构造字典，键是年，值是每个月的数据的列表形式
        year_dict = {}
        for year in years:
            if year not in year_dict:
                year_dict[year] = []
        # 现在单纯的将每一年的各个月份的数值填入字典的值中
        for key, value in now_dict.items():
            for year in years:
                if year in key:
                    year_dict[year].append(value)
        # 构造新列表统计每一年中最严重的月份
        end_dict = {}
        for year in years:
            end_dict[year] = []
        for year in years:
            max_value = max(year_dict[year])
            for i in range(len(year_dict[year])):
                # 返回对应的下标
                if year_dict[year][i] == max_value:
                    end_dict[year].append(months[i])
        for key, value in end_dict.items():
            if len(value) == 1:
                print("{} was the worst month in 1 years ({})".format(key, value[0]))
            else:
                for i in range(len(value)):
                    print("{} was the worst month in 1 years ({})".format(key, value[i]))
    question1(path)
    question2(path)


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided. You can comment/uncomment tests if you want.

if __name__ == '__main__':
    # test on data from the Civic monitoring station
    analyse('aqi_data_civic.csv')

    # test on data from the Florey monitoring station
    analyse('aqi_data_florey.csv')

    # test on data from the Monash monitoring station
    analyse('aqi_data_monash.csv')

