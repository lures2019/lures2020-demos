import requests
import csv

def get_cookie():
    cookie = requests.get("https://www.lagou.com/jobs/list_%E4%BC%9A%E8%AE%A1?labelWords=&fromSearch=true&suginput=", headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},allow_redirects=False).cookies
    return cookie

def get_information(i):
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    headers = {
        'origin': 'https://www.lagou.com',
        'referer': 'https://www.lagou.com/jobs/list_%E4%BC%9A%E8%AE%A1?labelWords=&fromSearch=true&suginput=',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'cookie': 'RECOMMEND_TIP=true; user_trace_token=20201202174738-aae4bb63-e0e3-4e26-923c-7074202dcf3c; LGUID=20201202174738-a07c9de1-9cb8-43e7-946a-c8206a777b75; _ga=GA1.2.1342855003.1606902458; JSESSIONID=ABAAAECABFAACEA6F8452BC43EFE6065C5B0DBE4576A4BE; WEBTJ-ID=20210103231450-176c8d0b930217-020e8e98bb0d6c-3e604809-1049088-176c8d0b9312f2; sensorsdata2015session=%7B%7D; LGSID=20210103231451-cbb1fbe2-2b4b-4253-bcf4-f55cf00b0a25; _gid=GA1.2.1792367896.1609686892; index_location_city=%E5%85%A8%E5%9B%BD; X_MIDDLE_TOKEN=6cc9ad2985a7ad777f79728823d9cf99; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1609686891,1609687000,1609687128; gate_login_token=ea8ec32a4ce2093050bac9dcfc6400f7a2d9f71fa8d864c366566e951551b6ff; _putrc=BB0CCD8EF0244CCC123F89F2B170EADC; login=true; unick=%E7%8E%8B%E6%99%BA%E8%B6%85; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=29; privacyPolicyPopup=false; TG-TRACK-CODE=index_search; _gat=1; X_HTTP_TOKEN=05fa1fb41570ec80249096906143d296feb32ed90d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216812862%22%2C%22first_id%22%3A%2217622d9a53194-0dd07a71b38066-3f6b4b05-1049088-17622d9a5323b4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2286.0.4240.198%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217622d9a53194-0dd07a71b38066-3f6b4b05-1049088-17622d9a5323b4%22%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1609690943; LGRID=20210104002223-cea8ebda-543b-4f4f-8d80-ce8399b038b5; SEARCH_ID=49a00073151a42c9acfdf3dab92e3641'
    }
    data = {
        'first': 'true',
        'pn': i,
        'kd': '会计'
    }
    # 根据网页解析知道是post方法
    response = requests.post(url=url, headers=headers, params=data,cookies=get_cookie())
    # 设置编码，万能解码
    response.encoding = response.apparent_encoding
    # 使用response.json()提取到数据所在的键
    results = response.json()["content"]["positionResult"]["result"]

    # 设置编码格式以及用写方式打开文件
    f = open("财汇专业招聘岗位信息表.csv", mode='a+', newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)

    # 依次遍历
    for result in results:
        positionName = result["positionName"]               # 职位名称
        companyFullName = result["companyFullName"]         # 公司全称
        companySize = result["companySize"]                 # 公司人数
        createTime = result["createTime"]                   # 发布时间
        city = result["city"]                               # 工作城市
        salary = result["salary"]                           # 薪资待遇
        workYear = result["workYear"]                       # 工作经验
        education = result["education"]                     # 学历要求
        positionAdvantage = result["positionAdvantage"]     # 职位优势

        csv_write.writerow([positionName, companyFullName, companySize, createTime, city, salary, workYear, education,positionAdvantage])

if __name__ == '__main__':
    # 设置编码格式以及用写方式打开文件
    f = open("财汇专业招聘岗位信息表.csv", mode='w', newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['职位名称', '公司全称', '公司人数', '发布时间', '工作城市', '薪资待遇', '工作经验', '学历要求', '职位优势'])

    for i in range(1,31):
        try:
            get_information(i)
            print("第{}页信息爬取完毕！".format(i))
        except Exception as error:
            print(error)