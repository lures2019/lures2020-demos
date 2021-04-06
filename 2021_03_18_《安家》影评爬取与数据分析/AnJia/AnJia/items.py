# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # 用于存储评论信息
    comments = scrapy.Field()
    # 用于存储觉得[有用]的人数信息
    number = scrapy.Field()
    # 用于存储用户id
    ids = scrapy.Field()
    # 用于存储自己状态[看过/在看/想看]
    status = scrapy.Field()
    # 存储自己的想法[力荐/推荐……]
    rating = scrapy.Field()
    # 存储评论发表时间
    time = scrapy.Field()
