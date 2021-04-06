# -*- coding: utf-8 -*-
import scrapy
import logging
# 用logging得到的实例，输出当前warning的py文件位置
"""2021-03-19 08:52:36 [myspider.spiders.itcast] WARNING: """
logger = logging.getLogger(__name__)

class ItcastSpider(scrapy.Spider):
    # 爬虫名
    name = 'itcast'
    # 允许爬虫范围
    allowed_domains = ['itcast.cn']
    # 最开始请求的url地址
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        # 处理start_urls地址对应的响应
        # ret1 = response.xpath("//ul/li/div[@class='li_txt']/h3/text()").getall()
        # print(ret1)
        # 分组
        li_list = response.xpath("//div[@class='tea_con']//li")
        for li in li_list:
            item = {}
            item["name"] = li.xpath(".//h3/text()").extract_first()
            item["title"] = li.xpath(".//h4/text()").extract()[0]
            item["coment"] = li.xpath(".//p/text()").get()
            # print(item)
            # 减小内存占用,返回对象类型只能有Request/BaseItem/dict/None
            logger.warning(item)
            yield item


