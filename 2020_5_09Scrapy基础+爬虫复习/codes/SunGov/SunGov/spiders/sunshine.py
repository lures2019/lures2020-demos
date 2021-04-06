# -*- coding: utf-8 -*-
import scrapy


class SunshineSpider(scrapy.Spider):
    name = 'sunshine'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']

    def parse(self, response):
        
        pass
