# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Book365Item(scrapy.Item):
    title = scrapy.Field()
    download_link = scrapy.Field()
