# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class BiqugePipeline(object):
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        with open('{}.txt'.format(self.items[0]['book_name']), 'w', encoding='utf-8') as f:
            self.items.sort(key=lambda j: j['order'])
            for item in self.items:
                f.write(item['capter_name'] + '\n')
                for i in item['text']:
                    f.write(i + '\n')
            f.write('\n\n\n')



