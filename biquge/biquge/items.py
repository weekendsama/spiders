# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeItem(scrapy.Item):
    book_name = scrapy.Field()
    capter_name = scrapy.Field()
    detail_page = scrapy.Field()
    text = scrapy.Field()
    order = scrapy.Field()
