# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from meituricom.items import MeituricomItem

class MeituriSpider(CrawlSpider):
    name = 'meituri'
    allowed_domains = ['meituri.com']
    start_urls = ['https://www.meituri.com/jigou/']

    rules = (
        Rule(LinkExtractor(allow=r'.+/x/\d'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        cate = response.xpath('//div[@class="fenlei"]/h1/text()').get()
        names = response.xpath('//p[@class="biaoti"]/a/text()').getall()
        urls = response.xpath('//p[@class="biaoti"]/a/@href').getall()
        for name, url in zip(names, urls):
            if any(each in cate for each in ['The Black Alley', 'IESS', 'RQ-STAR']):
                continue
            item = MeituricomItem()
            item['name'] = name
            item['catename'] = cate
            yield scrapy.Request(url, callback=self.parse_detial, meta={'item': item})

    def parse_detial(self, response):
        item = response.meta['item']
        downloads = response.xpath('//div[@class="content"]/img/@src').getall()
        next_page = response.xpath('//div[@id="pages"]/a[last()]/@href').get()
        item['download_url'] = downloads
        yield item
        if next_page != response.url or not next_page:
            yield scrapy.Request(next_page, callback=self.parse_detial, meta={'item': response.meta['item']})
