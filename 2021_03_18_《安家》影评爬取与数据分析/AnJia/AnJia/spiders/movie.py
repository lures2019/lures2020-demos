# -*- coding: utf-8 -*-
import scrapy
from logging import getLogger
from AnJia.items import AnjiaItem
import time


# 生成迭代对象，进行日志处理
logger = getLogger(__name__)

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['https://movie.douban.com/']
    # 这是爬取的首页链接
    start_urls = []
    # 豆瓣只开放500条评论
    for i in range(0, 481, 20):
        # 看过的url
        url = "https://movie.douban.com/subject/30482003/comments?start={}&limit=20&status=P&sort=new_score".format(i)
        # 在看的url
        url1 = "https://movie.douban.com/subject/30482003/comments?start={}&limit=20&status=N&sort=new_score".format(i)
        # 想看的url
        url2 = "https://movie.douban.com/subject/30482003/comments?start={}&limit=20&status=F&sort=new_score".format(i)
        start_urls.append(url)
        start_urls.append(url1)
        start_urls.append(url2)

    # 下面是页面解析的函数,爬虫处理都在此函数中
    def parse(self, response):
        # 一次xpath提取出各div标签
        div_list = response.xpath('//div[@id="comments"]/div[@class="comment-item "]')
        # 二次xpath提取获取需要的标签信息
        for div in div_list:
            # 进行实例化操作
            item = AnjiaItem()
            item["comments"] = div.xpath('./div[@class="comment"]/p[@class=" comment-content"]/span[@class="short"]/text()').get()
            item["number"] = div.xpath('./div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="votes vote-count"]/text()').get()
            item["ids"] = div.xpath('./div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').get()
            item["status"] = div.xpath('./div[@class="comment"]/h3/span[@class="comment-info"]/span[1]/text()').get()
            item["rating"] = div.xpath('./div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@title').get()
            item["time"] = div.xpath('./div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="comment-time "]/text()').get().strip()
            logger.warning(item)
            yield item
            print("已爬取20条！")
            time.sleep(2)


