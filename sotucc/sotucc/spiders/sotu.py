# -*- coding: utf-8 -*-
import scrapy
from sotucc.items import SotuccItem

class SotuSpider(scrapy.Spider):
    name = 'sotu'
    allowed_domains = ['sotu.cc']
    start_urls = ['http://www.sotu.cc/meinv/']

    def parse(self, response):
        target_urls = response.xpath('//div[@class="update_area"]/div/ul//li/a/@href').getall()
        titles = response.xpath('//div[@class="update_area"]/div/ul//li/a/@title').getall()
        for title, target_url in zip(titles, target_urls):
            item = SotuccItem()
            item['title'] = title
            yield scrapy.Request(target_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        download_url = response.urljoin(response.xpath('//div[@class="content_left"]/img/@src').get())
        next_pager = response.xpath('//a[@class="next page-numbers"]/@href').get()
        item['download_url'] = download_url
        yield item
        if next_pager:
            yield scrapy.Request(next_pager, callback=self.parse_detail, meta={'item': item})
