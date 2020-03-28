"""
    选取10个招聘会进行爬取，http://www.bjbys.net.cn/zph/
    需求：爬取到所属行业、所在地址、职位详情、招聘人数、工资以及学历并存进数据库
"""
import requests
import re
import parsel
import pymysql
import time
# 禁止警告的添加
import urllib3
urllib3.disable_warnings()

def get_more_urls(page):
    headers = {
        'Cookie': '_ga=GA1.3.1863494307.1585202394; _gid=GA1.3.1355359632.1585202394; UM_distinctid=171156cf5e5194-09d41cddbb8fc6-376b4502-ff000-171156cf5e6e3; zg_did=%7B%22did%22%3A%20%22171156cf661129-04bb17e1ac707b-376b4502-ff000-171156cf662796%22%7D; Hm_lvt_c4b34eec3877ae7676849bfa3056b1bb=1585220336; Hm_lpvt_c4b34eec3877ae7676849bfa3056b1bb=1585220336; CNZZDATA4893697=cnzz_eid%3D653795452-1585216144-%26ntime%3D1585216144; 214_vq=10; zg_f93934739bc3442688ace74ff578337c=%7B%22sid%22%3A%201585220344877%2C%22updated%22%3A%201585220992633%2C%22info%22%3A%201585202394729%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.bjbys.net.cn%22%7D',
        'Host': 'job.bjbys.net.cn',
        'Referer': 'https://job.bjbys.net.cn/student/jobfair/fairdetails.html?fairId=EjUvEkD6QdUEHGhh1zYsTN',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    # 不加params最多显示10条数据
    params = {
        # 每页展示16条数据
        'limit': '16',
        'offset': str(page)  # 设置换页的参数
    }
    new_urls = get_main_urls()
    urls = []
    for i in range(len(new_urls)):
        url = new_urls[i].replace(r'fairdetails.html?','corp?')
        response = requests.get(url=url, headers=headers, params=params, verify=False)
        response.encoding = response.apparent_encoding
        results = response.json()['companyList']
        # 双选会会场首页
        for result in results:
            company_name = result['name']
            name = str(re.findall("b'(.*?)'", str(bytes(company_name, encoding="utf-8")))[0]).replace(r'\x', '%')
            urls.append('https://job.bjbys.net.cn/student/m/api/jobfair/jobs?fairId=EjUvEkD6QdUEHGhh1zYsTN&jobType=&areaCode=&jobName=' + name + '&monthPay')
    return(urls)


def get_message(page):
    urls = get_more_urls(page)
    connection = pymysql.connect(
        host='localhost',  # 服务器的ip
        port=3306,  # 数据库开发的端口
        user='root',  # 用户名
        password='wangzhi20001115',  # 密码
        database='position_message',  # 需要使用的数据库
    )
    # 获取执行命令的游标
    cursor = connection.cursor()
    for url in urls:
        response = requests.get(url=url,verify=False)
        response.encoding = response.apparent_encoding
        html = response.json()['data']['list']
        data = [[] for i in range(len(html))]
        for i in range(len(html)):
            data[i].append(html[i]['jobId'])                 # 获取id
        datas = [[] for i in range(len(data))]
        for j in range(len(data)):
            url = 'https://job.bjbys.net.cn/student/jobs/'+ str(data[j][0]) + '/detail.html'
            headers = {
                'Cookie': 'SESSION=1f6acb26-bbd0-4fdd-a934-901a41f9d15e; TS01807f27=01886fbf6ed57a917269334b3057daf592b5e28860494430a8a65e87fed97fdb386cff1ec16ba22e20554022e89453764b8551d2e641ddb12575bb55179a50332b4c4e77c7e25c052e05e50fcb2c11855275e49ad9; XSRF-CCKTOKEN=e89c8e3304eb3aa92778d125a0bffa8c; TS01179b35=01886fbf6ec6ad030fa44006b26e1f9ad12ea4b29e494430a8a65e87fed97fdb386cff1ec15927f2187479dc2bb019a578f89d0c62653e61fa3d66818cf1c9db12d9d60bae; _ga=GA1.3.1863494307.1585202394; _gid=GA1.3.1355359632.1585202394; UM_distinctid=171156cf5e5194-09d41cddbb8fc6-376b4502-ff000-171156cf5e6e3; zg_did=%7B%22did%22%3A%20%22171156cf661129-04bb17e1ac707b-376b4502-ff000-171156cf662796%22%7D; Hm_lvt_c4b34eec3877ae7676849bfa3056b1bb=1585220336; CHSICC02=!JFfaoz1NX5Pf97cGGYWrKFjgWJfD/0NtlCIm3C73BH/3r5nRoPU2JNuzL1BeBlmH+V+qWCxaSNKjlQ==; CHSICC01=!0w/YP1ZSX778DT0GGYWrKFjgWJfD/3um33mQ1+9qd5UWa3EBjEh5yjOTvCg59rfHVpB3JujqdJGJpw==; CNZZDATA1278653655=1404685713-1585200783-null%7C1585277795; TS01786ae5=01886fbf6edd04e844cf17d68f8e5a8ae08ae23dc8247b33cd08d3c3acf5df448d818a9a15ece4b249abdb9e74fff60085bef8737fda9da93179c37efc557bb49d860df844; Hm_lvt_96e6f7018e1069595ef7211c59603cfe=1585279817,1585279825,1585279904,1585280363; _gat=1; zg_f93934739bc3442688ace74ff578337c=%7B%22sid%22%3A%201585279694950%2C%22updated%22%3A%201585280513662%2C%22info%22%3A%201585202394729%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.bjbys.net.cn%22%7D; Hm_lpvt_96e6f7018e1069595ef7211c59603cfe=1585280514',
                'Host': 'job.bjbys.net.cn',
                'Referer': 'https://job.bjbys.net.cn/student/m/jobfair/jobs.html?fairId=EjUvEkD6QdUEHGhh1zYsTN&jobName=a01%E5%8C%97%E4%BA%AC%E7%AB%8B%E8%81%8C%E6%95%99%E8%82%B2%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }
            response = requests.get(url=url, headers=headers, verify=False)
            response.encoding = response.apparent_encoding
            select = parsel.Selector(response.text)
            # 职位名称 jobName
            datas[j].append(select.xpath('//li[@id="jobName"]/text()').get())
            # 是否全职 is_not_full_time
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-left fl"]/div[@class="job clearfix basic-color-bg4"]/ul[@class="work clearfix"]/li/span/text()').get())
            # 薪资 salary
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-left fl"]/div[@class="job clearfix basic-color-bg4"]/ul[@class="salary clearfix"]/li[1]/span/text()').get())
            # 学历要求 education
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-left fl"]/div[@class="job clearfix basic-color-bg4"]/ul[@class="salary clearfix"]/li[3]/span/text()').get())
            # 招聘人数 recruitment
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-left fl"]/div[@class="job clearfix basic-color-bg4"]/ul[@class="salary clearfix"]/li[5]/span/span/text()').get())
            # 发布时间 update_time
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-left fl"]/div[@class="job clearfix basic-color-bg4"]/ul[@class="salary clearfix"]/li[6]/span/text()').get())
            # 专业要求 professional_requirements
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-left fl"]/div[@class="job clearfix basic-color-bg4"]/div[@class="major"]/text()').get())
            # 职位详情 job_details
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-left fl"]/div[@class="details"]/div[@class="jobdetail-box"]/div[@class="mainContent mainContent-geshi"]/text()').get())
            # 公司名称 company_name
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-right fr"]/div[@class="company"]/p[@id="corpName"]/span[@id="realCorpName"]/text()').get())
            # 所属行业 industry
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-right fr"]/div[@class="company"]/ul[@class="details"]/li[2]/span[@id="mainindustries"]/text()').get())
            # 公司性质 company_type
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-right fr"]/div[@class="company"]/ul[@class="details"]/li[4]/span[@class="show fr"]/text()').get())
            # 公司规模 company_size
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-right fr"]/div[@class="company"]/ul[@class="details"]/li[5]/span[@class="show fr"]/text()').get())
            # 公司地址 company_address
            datas[j].append(select.xpath('//div[@id="content"]/div[@class="content-wrap"]/div[@class="con-right fr"]/div[@class="company"]/ul[@class="details"]/li[7]/span[@id="companyNameMap"]/text()').get())
        for d in datas:
            cursor.execute('insert into lagou(jobName,is_not_full_time,salary,education,recruitment,update_time,professional_requirements,job_details,company_name,industry,company_type,company_size,company_address) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',d)
        connection.commit()  # 提交修改
        time.sleep(2)
    cursor.close()  # 关闭游标 关闭链接
    connection.close()



def get_main_urls():
    url = 'http://www.bjbys.net.cn/zph/'
    headers = {
        'Cookie': '_ga=GA1.3.1863494307.1585202394; _gid=GA1.3.1355359632.1585202394; UM_distinctid=171156cf5e5194-09d41cddbb8fc6-376b4502-ff000-171156cf5e6e3; zg_did=%7B%22did%22%3A%20%22171156cf661129-04bb17e1ac707b-376b4502-ff000-171156cf662796%22%7D; Hm_lvt_c4b34eec3877ae7676849bfa3056b1bb=1585220336; Hm_lpvt_c4b34eec3877ae7676849bfa3056b1bb=1585220336; CNZZDATA4893697=cnzz_eid%3D653795452-1585216144-%26ntime%3D1585216144; zg_f93934739bc3442688ace74ff578337c=%7B%22sid%22%3A%201585220344877%2C%22updated%22%3A%201585223184553%2C%22info%22%3A%201585202394729%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.bjbys.net.cn%22%7D; 214_vq=13',
        'Host': 'www.bjbys.net.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers,verify=False)
    response.encoding = response.apparent_encoding
    select = parsel.Selector(response.text)
    results = select.xpath('//div/table/tbody/tr/td[4]')
    urls = []
    for i in range(len(results)):
        is_not_run = results[i].xpath('a/text()').get()
        # 选择正在进行招聘的会场
        if(is_not_run == '进入会场'):
            urls.append(results[i].xpath('a/@href').get())
    return(urls)


if __name__ == '__main__':
    page = int(input("请输入爬取的页数:(一定要是正整数！)"))
    for i in range(page):
        get_message(i+1)
        print("第{}页信息保存到数据库中！".format(str(i+1)))
        time.sleep(2)


