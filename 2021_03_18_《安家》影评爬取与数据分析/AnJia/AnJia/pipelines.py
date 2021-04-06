# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from logging import getLogger
import json

logger = getLogger(__name__)

class AnjiaPipeline(object):
    def process_item(self, item, spider):
        # 将数据保存为json格式
        with open("《安家》短评.json",mode="a+",encoding="utf-8") as f:
            item = dict(item)
            f.write(json.dumps(item,indent=2,ensure_ascii=False))
        f.close()
        return item
