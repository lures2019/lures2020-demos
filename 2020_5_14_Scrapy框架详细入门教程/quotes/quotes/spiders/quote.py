# -*- coding: utf-8 -*-
import scrapy
import urllib.parse

class QuoteSpider(scrapy.Spider):
    # name是项目名
    name = 'quote'
    # 只爬取指定域名下面的网页
    allowed_domains = ['toscrape.com']
    # 起始网址，发送一个request请求
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        """
            默认起始网址的相应，会传入到parse方法
            response响应体
        """
        divs = response.css(".quote")
        for div in divs:
            text = div.css('.text').extract_first()
            author = div.css('.author').extract_first()
            tags = div.css('.tags').extract()

            # yield返回的内容，必须是字典(dict)或者是item类型的数据
            # return 返回一次，yield返回很多次直到截止
            yield dict(text=text,author=author,tags=tags)
        next_page = response.css('.next a::attr(href)').extract_first()
        if next_page:
            # url拼接，构建完整的url
            next_url = urllib.parse.urljoin(response.url,next_page)
            # 产生一个request对象
            # 响应体指定给谁
            yield scrapy.Request(next_url,callback=self.parse)