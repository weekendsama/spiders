# -*- coding: utf-8 -*-
import scrapy
from xsnvshencom.items import XsnvshencomItem

class XsnvshenSpider(scrapy.Spider):
    name = 'xsnvshen'
    allowed_domains = ['xsnvshen.com']
    start_urls = ['https://www.xsnvshen.com/album/?p=1']

    def parse(self, response):
        tities = response.xpath('//div[@class="camLiCon"]/div/p/a/text()').getall()
        urls = response.xpath('//div[@class="camLiCon"]/div/p/a/@href').getall()
        for title, raw_url in zip(tities, urls):
            detail_url = 'https://www.xsnvshen.com' + raw_url
            item = XsnvshencomItem()
            item['title'] = title
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})
        next_page = response.xpath('//div[@id="pageNum"]/a[last()]/@data-page').get()
        now_page = response.url.split('=')[-1]
        if next_page is not now_page or None:
            new_url = response.url.split('=')[0] + '=' +  next_page
            yield scrapy.Request(new_url, callback=self.parse)

    def parse_detail(self,response):
        item = response.meta['item']
        url = []
        raw_download_urls = response.xpath('//ul[contains(@class,"clearfix") and contains(@class, "gallery")]//li/div/img/@src').getall()
        for raw_download_url in raw_download_urls:
            download_url = response.urljoin(raw_download_url).split('/')
            raw_url = 'https://img.xsnvshen.com/' + '/'.join(download_url[-4:])
            url.append(raw_url)
        item['urls'] = url
        yield item
