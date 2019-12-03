# -*- coding: utf-8 -*-
import scrapy
from xiurenorg.items import XiurenorgItem


class XiurenSpider(scrapy.Spider):
    name = 'xiuren'
    allowed_domains = ['xiuren.org']
    start_urls = ['http://www.xiuren.org/category/XiuRen.html']

    def parse(self, response):
        detail_page = response.xpath('//div[@class="loop"]/div/a/@href').getall()
        names = response.xpath('//div[@class="loop"]/div/a/@title').getall()
        page_num = response.xpath('//div[@id="page"]/span/text()').get().split('/')
        for detail_url, name in zip(detail_page, names):
            item = XiurenorgItem()
            item['name'] = name
            item['detail_url'] = detail_url
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})
        if page_num[0] != page_num[-1]:
            new_url = r'http://www.xiuren.org/category/XiuRen-{}.html'.format(str(int(page_num[0]) + 1))
            yield scrapy.Request(new_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        download_urls = response.xpath('//span[@class="photoThum"]/a/@href').getall()
        item['download_urls'] = download_urls
        yield item
