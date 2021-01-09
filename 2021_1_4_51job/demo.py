import requests
import re
import json
import os
import csv

def get_information(url,kd):
    url = url
    kd = kd
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    datas = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>', response.text)[0]
    datas_json = json.loads(datas)["engine_search_result"]
    # 打开csv文件
    fp = open(path + '/' + "51job{}职位信息.csv".format(kd),mode="a+",encoding="utf-8-sig",newline="")
    csv_write = csv.writer(fp)

    # 得到json形式数据后，开始进行提取信息
    for data in datas_json:
        # 职位名称
        job_name = data["job_name"]
        # 公司名称
        company_name = data["company_name"]
        # 薪资水平
        providesalary_text = data["providesalary_text"]
        # 职位要求
        attribute_text = data["attribute_text"]
        # 发布时间
        updatedate = data["updatedate"]
        # 工作待遇
        jobwelf = data["jobwelf"]
        # 员工数目
        companysize_text = data["companysize_text"]
        # 公司领域
        companyind_text = data["companyind_text"]
        # 公司性质
        companytype_text = data["companytype_text"]

        # 将以上数据写入csv文件中
        for i in range(len(job_name)):
            csv_write.writerow([job_name,company_name,providesalary_text,attribute_text,updatedate,
                                jobwelf,companysize_text,companyind_text,companytype_text])
    # 关闭文件
    f.close()

if __name__ == '__main__':
    path = "招聘信息"
    if not os.path.exists(path):
        # 不存在此目录则创建一个
        os.mkdir(path)
    keyword = input("请输入查询得岗位：")
    f = open(path + '/' + "51job{}职位信息.csv".format(keyword),mode="w",encoding="utf-8-sig",newline="")
    csv_write = csv.writer(f)
    csv_write.writerow(["职位名称","公司名称","薪资水平","职位要求","发布时间","工作待遇","员工数目","公司领域","公司性质"])
    for i in range(1,41):
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(keyword,i)
        # 调用子函数
        get_information(url,keyword)
        print("第{}页信息写入到csv文件中！".format(i))

    print("{}职位信息爬取完毕！".format(keyword))