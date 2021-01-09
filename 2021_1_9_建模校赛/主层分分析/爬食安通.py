import requests
import parsel
import re
import os
import csv

url = 'http://www.eshian.com/sat/yyss/datapage'
# 是post请求，因此需要提交表单
headers = {
    'Host': 'www.eshian.com',
    'Origin': 'http://www.eshian.com',
    'Referer': 'http://www.eshian.com/sat/yyss/list',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    "Cookie": "mediav=%7B%22eid%22%3A%22404701%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22!1Iqz%5DxAN*9%23S'wE%60TB'%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22!1Iqz%5DxAN*9%23S'wE%60TB'%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; yunsuo_session_verify=fc09074b93879c3ed7479e87f398fde9; JSESSIONID=3E3B419BD2D39275C5A8CD27CD68E48E; __51cke__=; Hm_lvt_45e883a2828739c24ed6025739ec9fae=1609765961,1609937008; Hm_lvt_fd540e193a5c4f0b04c640ccb812f17c=1609765961,1609937008; Qs_lvt_181391=1609765960%2C1609937008; mediav=%7B%22eid%22%3A%22404701%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22!1Iqz%5DxAN*9%23S'wE%60TB'%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22!1Iqz%5DxAN*9%23S'wE%60TB'%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; looyu_id=984c6d4635fe243456b970908d8b6073_10031053%3A2; looyu_10031053=v%3A84a05316b3126cff82869c928d120a4c%2Cref%3A%2Cr%3A%2Cmon%3A//m6816.talk99.cn/monitor%2Cp0%3Ahttp%253A//www.eshian.com/sat/standard/standardlist/0%253Finfo%253D%2525E9%252585%2525B8%2525E5%2525A5%2525B6; _99_mon=%5B0%2C0%2C0%5D; __tins__19161105=%7B%22sid%22%3A%201609937007725%2C%20%22vd%22%3A%2011%2C%20%22expires%22%3A%201609939561311%7D; __51laig__=11; Hm_lpvt_45e883a2828739c24ed6025739ec9fae=1609937761; Hm_lpvt_fd540e193a5c4f0b04c640ccb812f17c=1609937761; Qs_pv_181391=1533656344499763000%2C3137875606468300300%2C1156048555940104200%2C3402579854603794400%2C1559155956166264800"
}
"""上面的东西都不用变化"""

def get_pages(kd):
    data = {
        'pageNo': '1',  # 当前页,第二页
        'foodName': kd  # 食物名称
    }
    response = requests.post(url, headers=headers, params=data)
    # 设置万能解码
    response.encoding = response.apparent_encoding
    # 现在开始提取页数
    select = parsel.Selector(response.text)
    # ['\r\n\t\t', ' / 5 ', '\r\n\t']
    pages = int(select.xpath('//div[@class="page-nav text-center"]/span[5]/text()').getall()[1].replace("/", "").strip())
    # 返回页数，方便后面的查询
    return pages


def get_one_cell_information(url,kd):
    url = url
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    # 构造xpath提取规则
    select = parsel.Selector(response.text)
    trs = select.xpath('//table[@class="table table-bordered table-fixed td-word-break yp-table-pull"]/tbody/tr')
    # 第一列营养素的值
    value1s = []
    # 第二列营养素的值
    value2s = []
    for tr in trs:
        # 需要单独处理，数据不能直接用
        value1s.append(tr.xpath('//td[1]').getall())
        value2s.append(tr.xpath('//td[2]').getall())
    # 因为本身就是列表，所以进行操作的时候取的是第一个元素
    value1 = []
    for value in value1s[0]:
        # 决定使用正则表达式进行提取
        value_now = re.findall('<td class="ndata_rb">(.*?)</td>',value)
        # 如果value_now的长度是0则代表需要更换提取方式，如果是1，则取第一个元素
        if len(value_now) == 0:
            value_now = re.findall('<td>(.*?)</td>',value)
            # 还有一列提取不成功
            if len(value_now) == 0:
                value_now = value.replace(r"<td>","").replace(r"</td>","").strip()
                value1.append(value_now)
            else:
                value1.append(value_now[0])
        else:
            value1.append(value_now[0])
    # 需要对values2做同样的操作
    value2 = []
    for value in value2s[0]:
        # 决定使用正则表达式进行提取,和values1提取不一样的地方就是td的类名不一致
        value_now = re.findall('<td class="ndata_b">(.*?)</td>',value)
        # 如果value_now的长度是0则代表需要更换提取方式，如果是1，则取第一个元素
        if len(value_now) == 0:
            value_now = re.findall('<td>(.*?)</td>',value)
            # 还有一列提取不成功
            if len(value_now) == 0:
                value_now = value.replace(r"<td>","").replace(r"</td>","").strip()
                value2.append(value_now)
            else:
                value2.append(value_now[0])
        else:
            value2.append(value_now[0])

    # 最终合并成1个列表
    end_value = []
    # 经过上述步骤，一页信息已经爬取完毕
    for i in range(len(value1)):
        # 去除无关干扰
        value1[i].replace(r"Tr","").replace(r"—","").replace(r"…","").strip()
        value2[i].replace("Tr","").replace("—","").replace("…","").strip()
        end_value.append(value1[i])
        end_value.append(value2[i])
    # 直接写入csv文件
    f = open(path + '/' + '食物营养指标.csv',mode="a+",encoding="utf-8-sig",newline="")
    csv_write = csv.writer(f)
    csv_write.writerow(end_value)
    f.close()

# 1页数据已经爬好了，现在问题是并不是所有数据都是需要的，需要的是带均值的产品，且找到直接跳出该页面，否则用第一个来替代
def choose_real_url(url,kd):
    # 获取关键词得到的页数信息
    pages = get_pages(kd)
    # 存放总链接和总标题
    all_hrefs = []
    all_titles = []
    # 开始遍历pages
    for i in range(pages):
        data = {
            'pageNo': i,  # 当前页
            'foodName': kd  # 食物名称
        }
        response = requests.post(url, headers=headers, params=data)
        # 设置万能解码
        response.encoding = response.apparent_encoding
        # 现在开始提取页数
        select = parsel.Selector(response.text)
        # 提取单元格的链接以及标题
        hrefs = select.xpath('//table[@class="table table-bordered table-fixed table-text-center table-link td-word-break"]/tbody/tr/td/a/@href').getall()
        titles = select.xpath('//table[@class="table table-bordered table-fixed table-text-center table-link td-word-break"]/tbody/tr/td/a/text()').getall()
        real_links = ['http://www.eshian.com' + i for i in hrefs]
        # 将信息写入大列表
        for i in range(len(hrefs)):
            all_hrefs.append(real_links[i])
            all_titles.append(titles[i])
    # 打印结果
    # 开始遍历all_titles，看能否有kd（均值）的数据
    # 设置状态
    status = False
    for i in range(len(all_titles)):
        if all_titles[i] == "{}（均值）".format(kd):
            url = all_hrefs[i]
            # 调用函数
            get_one_cell_information(url,kd)
            status = True
            break
    # 代表遍历后都没有找到这个信息
    if status == False:
        url = all_hrefs[0]
        get_one_cell_information(url,kd)
    print("{}信息已经录入csv文件！".format(kd))



if __name__ == '__main__':
    # get_pages()
    path = "新爬内容"
    if not os.path.exists(path):
        # 不存在此目录则创建一个
        os.mkdir(path)
    # 查询的关键词
    keywords = ['面条', '馒头', '油饼', '稻米', '糯米', '玉米', '小米', '马铃薯', '红薯', '粉丝', '黄豆', '豆腐', '豆浆',
                '腐竹', '豆腐干', '素什锦', '豆沙', '蚕豆', '核桃', '板栗', '花生', '葵花子', '西瓜子', '白萝卜', '胡萝卜', '黄豆芽',
                '绿豆芽', '茄子', '番茄', '辣椒', '甜椒', '冬瓜', '黄瓜', '苦瓜', '南瓜', '丝瓜', '西葫芦', '大蒜', '洋葱', '韭菜', '大白菜',
                '小白菜', '菜花', '菠菜', '芹菜茎', '香菜', '藕', '芋头', '姜', '草菇', '金针菇', '平菇', '木耳', '香菇', '海带', '羊肉', '鸡',
                '鸭', '鹅', '牛乳', '酸奶', '奶油', '鸡蛋', '鸭蛋', '皮蛋', '咸鸭蛋', '鹌鹑蛋', '草鱼', '黄鳝', '鲤鱼', '鲫鱼', '带鱼', '对虾',
                '河蟹', '鲍鱼', '螺', '鱿鱼', '菜籽油', '豆油', '花生油', '色拉油', '苹果', '橘子', '樱桃', '香蕉',
                '蜜桃', '杏', '草莓', '葡萄', '猕猴桃', '西瓜', '芒果', '梨', '牛肉', '猪肉', '驴肉', '火鸡肉', '牛油', '羊油', '猪油', '奶粉', '奶酪']
    # 创建此文件
    f = open(path + '/' + "食物营养指标.csv", newline="", encoding='utf-8-sig', mode='w')
    csv_write = csv.writer(f)
    # 添加指标后一劳永逸
    csv_write.writerow(
        ['食品中文名', '食品英文名', '食品分类', '可食部', '来源', '产地', '营养素含量（100克可食部食品中的含量）', '蛋白质(克)', '脂肪(克)', '饱和脂肪酸(克)', '反式脂肪酸(克)',
         '单不饱和脂肪酸(克)', '多不饱和脂肪酸(克)', '胆固醇(毫克)', '碳水化合物(克)', '糖(克)', '乳糖(克)', '膳食纤维(克)', '可溶性膳食纤维(克)', '不溶性膳食纤维(克)',
         '钠(毫克)', '维生素A(微克视黄醇当量)', '维生素D(微克)', '维生素E(毫克α-生育酚当量)', '维生素K(微克)', '维生素B1（硫胺素）(毫克)', '维生素B2（核黄素）(毫克)',
         '维生素B6(毫克)', '维生素B12(微克)', '维生素C（抗坏血酸）(毫克)', '烟酸（烟酰胺）(毫克)', '叶酸(微克叶酸当量)', '泛酸(毫克)', '生物素(微克)', '胆碱(毫克)',
         '磷(毫克)', '钾(毫克)', '镁(毫克)', '钙(毫克)', '铁(毫克)', '锌(毫克)', '碘(微克)', '硒(微克)', '铜(毫克)', '氟(毫克)', '锰(毫克)', 'δ-E(毫克)',
         '(β-γ)-E(毫克)', 'α-E(毫克)', '胡萝卜素(微克)', '脂肪酸（总）(克)', '灰分(克)', '水分(克)', '能量(千卡)'])
    f.close()
    for kd in keywords:
        choose_real_url(url,kd)