# -*- coding: utf-8 -*-
import scrapy
from biquge.items import BiqugeItem


class Version1Spider(scrapy.Spider):
    name = 'version1'
    allowed_domains = ['biquge.com.cn']
    start_urls = ['https://www.biquge.com.cn/book/11007/']

    def parse(self, response):
        book_name = response.xpath('//div[@id="info"]/h1/text()').get()
        capters = response.xpath('//div[@id="list"]/dl/dd/a/text()').getall()
        detail_pages = response.xpath('//div[@id="list"]/dl/dd/a/@href').getall()
        order = 0
        for capter, detail_page in zip(capters, detail_pages):
            order += 1
            item = BiqugeItem()
            item ['order'] = order
            item['book_name'] = book_name
            item['capter_name'] = capter
            detail_page = r'https://www.biquge.com.cn{}'.format(detail_page)
            item['detail_page'] = detail_page
            yield scrapy.Request(detail_page, callback=self.cather, meta={'item': item})

    def cather(self, response):
        item = response.meta['item']
        text = response.xpath('string(//*[@id="content"])').get().split()
        item['text'] = text
        yield item
