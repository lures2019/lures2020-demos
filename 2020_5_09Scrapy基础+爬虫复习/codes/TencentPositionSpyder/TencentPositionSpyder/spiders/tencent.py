# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from ..items import TencentpositionspyderItem

logger = logging.getLogger(__name__)

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10']

    def parse(self, response):
        # 将str类型转换为json格式
        rets = json.loads(response.text)["Data"]['Posts']
        # 使用for循环进行遍历
        for ret in rets:
            item = TencentpositionspyderItem()
            item["RecruitPostName"] = ret["RecruitPostName"]
            item["CategoryName"] = ret["CategoryName"]
            item["Responsibility"] = ret["Responsibility"]
            item["LastUpdateTime"] = ret["LastUpdateTime"]
            logger.warning(item)
            yield item
        # 找到下一页url地址
        for i in range(2,940):
            next_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10'.format(i)
            # 构造Request对象实现翻页
            print("第{}页开始爬取！".format(i))
            yield scrapy.Request(
                next_url,
                callback = self.parse
            )

