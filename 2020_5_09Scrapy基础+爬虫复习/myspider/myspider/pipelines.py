# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        # if spider.name == "itcast":
        item["hello"] = "world"
        return item

class MyspiderPipeline1(object):
    def process_item(self, item, spider):
        print(item)
        # 多个piplines调用时必须要返回值

        return item