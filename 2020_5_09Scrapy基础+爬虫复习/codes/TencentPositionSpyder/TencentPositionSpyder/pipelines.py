# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient

client = MongoClient()
collection = client["tencent"]["招聘信息"]

class TencentpositionspyderPipeline(object):
    def process_item(self, item, spider):
        # 将返回的item保存为json格式
        with open("招聘信息.json",mode="a+",encoding="utf-8") as f:
            item = dict(item)
            f.write(json.dumps(item,indent=2,ensure_ascii=False))
        f.close()
        # 将item保存到MongoDB数据库中去
        collection.insert(item)
        return item
