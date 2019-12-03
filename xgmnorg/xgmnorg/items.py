# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XgmnorgItem(scrapy.Item):
    title = scrapy.Field()
    detail_link = scrapy.Field()
    info = scrapy.Field()
