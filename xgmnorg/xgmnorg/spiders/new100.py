# -*- coding: utf-8 -*-
import scrapy
from xgmnorg.items import XgmnorgItem

class New100Spider(scrapy.Spider):
    name = 'new100'
    allowed_domains = ['xgmn.org']
    start_urls = ['https://www.xgmn.org/new.html']

    def parse(self, response):
        though_info = response.xpath('//div[@class="dan1"]')
        detail_links = though_info.xpath('./a/@href').getall()
        titles = though_info.xpath('./a/@title').getall()
        real_infos = though_info.xpath('./a/b/text()').getall()
        for title, real_info, detail_link in zip(titles, real_infos, detail_links):
            real_detail_link = response.urljoin(detail_link)
            item = XgmnorgItem()
            item['title'] = title
            item['info'] = real_info
            item['detail_link'] = real_detail_link
            yield item

