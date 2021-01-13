"""
    - 2、获取每部影片的简介和影评（5“)
"""
import csv
import requests
import parsel

def get_article_links():
    # 加载csv文件信息
    f = open("爬取的数据/豆瓣250电影信息.csv", mode="r", encoding="utf-8")
    csv_reader = csv.reader(f)
    rows = [i for i in csv_reader]
    # 原csv文件中，我们只需要链接
    links = [row[-1] for row in rows[1:]]

    return links,rows



def write_original_csv(url,rows):
    url = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    # 设置解码和编码
    response.encoding = response.apparent_encoding
    # 构造xpath提取规则
    select = parsel.Selector(response.text)
    try:
        # 爬取简介和影评
        first_paragraph = select.xpath('//div[@id="link-report"]/span[1]/text()[1]').getall()[0].replace('\n',"").strip()
        second_paragraph = select.xpath('//div[@id="link-report"]/span[1]/text()[2]').getall()[0].replace('\n', "").strip()
        # 使用字符串拼接
        instruction = first_paragraph + second_paragraph
    except Exception as error:
        second_paragraph = ""
        instruction = select.xpath('//div[@id="link-report"]/span[1]/text()').getall()[0].replace('\n',"").strip()
        print(error)
    # 提取1页影评短信息
    comments = select.xpath('//div[@class="review-short"]/div[@class="short-content"]/text()[1]').getall()
    # 开始拼接吧
    film_comments = ""
    for x in comments:
        x_now = x.replace('\n', "").replace("(", "").replace("...", "").strip()
        film_comments += x_now
    for row in rows[1:]:
        # 能匹配到的话
        if url in row:
            row.append(instruction)
            row.append(film_comments)
        else:
            pass
    f = open("爬取的数据/豆瓣250电影信息.csv", mode="w", encoding="utf-8-sig", newline="")
    csv_write = csv.writer(f)
    for row in rows:
        csv_write.writerow(row)

if __name__ == "__main__":
    links,rows = get_article_links()
    rows[0].append("简介")
    rows[0].append("短评")
    for url in links:
        write_original_csv(url,rows)
        print(url)
    print("简介和影评加载完毕！")