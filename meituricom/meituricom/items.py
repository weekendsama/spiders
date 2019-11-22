# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituricomItem(scrapy.Item):
    catename = scrapy.Field()
    name = scrapy.Field()
    download_url = scrapy.Field()
