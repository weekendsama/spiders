# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json


class XgmnorgPipeline(object):
    def __init__(self):
        self.file = codecs.open(filename='info.csv', mode='w+', encoding='utf-8')

    def process_item(self, item, spider):
        res = dict(item)
        str = json.dumps(res, ensure_ascii=False)
        self.file.write(str)
        self.file.write(',\n')

    def close_spider(self, spider):
        self.file.close()
