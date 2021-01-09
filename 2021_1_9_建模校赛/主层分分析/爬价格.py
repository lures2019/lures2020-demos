import requests
import parsel
import csv

def get_price(kd):
    url = 'https://www.cnhnb.com/supply/?k={}'.format(kd)
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    select = parsel.Selector(response.text)
    # 得到食物的购买单位，如：元/箱 还是 元/斤 我们选择第一个为元/斤的食物
    units = select.xpath(
        '//a/div[@class="shops-card-content"]/div[@class="shops-text"]/div[@class="shops-price-bg"]/div[@class="shops-price"]/text()').getall()
    # 去除空格以及'\n'后存放到新的列表中
    right_units = []
    for unit in units:
        unit_now = unit.replace("\n", "").strip()
        right_units.append(unit_now)
    # 现在开始提取对应价格存放到列表中
    prices = select.xpath(
        '//a/div[@class="shops-card-content"]/div[@class="shops-text"]/div[@class="shops-price-bg"]/div[@class="shops-price"]/span/text()').getall()
    # 现在开始匹配，找到第一个单位为 元/斤的食物，将其价格得出
    for i in range(len(right_units)):
        if right_units[i] == '元/斤':
            return prices[i]
        else:
            pass


if __name__ == '__main__':
    keywords = ['面条', '馒头', '油饼', '稻米', '糯米', '玉米', '小米', '马铃薯', '红薯', '粉丝', '黄豆', '豆腐', '豆浆',
                '腐竹', '豆腐干', '素什锦', '豆沙', '蚕豆', '核桃', '板栗', '花生', '葵花子', '西瓜子', '白萝卜', '胡萝卜', '黄豆芽',
                '绿豆芽', '茄子', '番茄', '辣椒', '甜椒', '冬瓜', '黄瓜', '苦瓜', '南瓜', '丝瓜', '西葫芦', '大蒜', '洋葱', '韭菜', '大白菜',
                '小白菜', '菜花', '菠菜', '芹菜茎', '香菜', '藕', '芋头', '姜', '草菇', '金针菇', '平菇', '木耳', '香菇', '海带', '羊肉', '鸡',
                '鸭', '鹅', '牛乳', '酸奶', '奶油', '鸡蛋', '鸭蛋', '皮蛋', '咸鸭蛋', '鹌鹑蛋', '草鱼', '黄鳝', '鲤鱼', '鲫鱼', '带鱼', '对虾',
                '河蟹', '鲍鱼', '螺', '鱿鱼', '菜籽油', '豆油', '花生油', '色拉油', '苹果', '橘子', '樱桃', '香蕉',
                '蜜桃', '杏', '草莓', '葡萄', '猕猴桃',  '西瓜', '芒果', '梨','牛肉','猪肉','驴肉','火鸡肉','牛油','羊油','猪油','奶粉','奶酪']
    # 读取csv文件
    f = open('所有食物相关信息整合.csv',mode='r',encoding='utf-8')
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 加入价格后写入新文件
    fp = open("加上食物价格后完整信息.csv",mode='w',encoding='utf-8-sig',newline="")
    csv_write = csv.writer(fp)
    rows[0].append("元/斤")
    csv_write.writerow(rows[0])
    # 在每一列结尾加上食物价格
    try:
        for i in range(len(keywords)):
            if get_price(keywords[i]) == None:
                print("{}暂没有搜到！".format(keywords[i]))
                rows[i].append("")
            else:
                rows[i].append(get_price(keywords[i]))
            """
                打印为None的食物：
                '鱿鱼', '菜籽油', '豆油', '花生油', '色拉油','鲍鱼','带鱼', '对虾','黄鳝'
                这个能搜到，但是检索是None
                '马铃薯','大白菜'
            """
    except Exception as error:
        print(error)
        # 写入文件
    for row in rows[1:]:
        csv_write.writerow(row)
    fp.close()
