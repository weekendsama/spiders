# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MeituricomPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for download in item['download_url']:
            yield scrapy.Request(download, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        catename = item['catename']
        folder_name = item['name'].replace(r'/', '').rstrip()
        img_guid = request.url.split('/')[-1]
        img_name = img_guid
        filename = u'{0}/{1}/{2}'.format(catename, folder_name, img_name)
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('IMG download Failed')
        return item
