# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem

class MeizitunormalSpider(scrapy.Spider):
    name = 'meizitunormal'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/all/']

    def parse(self, response):
        years = response.xpath('//div[@class="year"]')
        for year in years:
            reallink = year.xpath('./following-sibling::ul[1]//li/p[2]/a/@href').getall()
            rawname = year.xpath('./following-sibling::ul[1]//li/p[2]/a/text()').getall()
            for name, url in zip(rawname, reallink):
                item = MeizituItem()
                item['year'] = year.xpath('./text()').get()
                item['name'] = name
                yield scrapy.Request(url, callback=self.parse_url, meta={'item': item})

    def parse_url(self, response):
        item = response.meta['item']
        download = response.xpath('//div[@class="main-image"]/p/a/img/@src').getall()
        last_page = response.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()').get()
        check_id = response.url.split('/')
        item['url'] = download
        yield item
        if int(check_id[-1]) > 500:
            new_url = response.url + '/2'
            yield scrapy.Request(new_url, callback=self.parse_url, meta={'item': item})
        else:
            if check_id[-1] is not last_page:
                new_page = str(int(check_id[-1]) + 1)
                new_url = '/'.join(check_id[:-1] + list(new_page))
                yield scrapy.Request(new_url, callback=self.parse_url, meta={'item': item})


