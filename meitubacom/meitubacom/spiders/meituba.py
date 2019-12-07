# -*- coding: utf-8 -*-
import scrapy
from meitubacom.items import MeitubacomItem

class MeitubaSpider(scrapy.Spider):
    name = 'meituba'
    allowed_domains = ['meituba.com']
    start_urls = ['http://www.meituba.com/xinggan/list81.html']

    def parse(self, response):
        '''
        解析目录页
        titles： 所有目录标题
        detail_urls ： 所有详情页URL
        '''
        titles = response.xpath('//div[@class="channel_list"]/ul//li/a/text()').getall()
        detail_urls = response.xpath('//div[@class="channel_list"]/ul//li/a/@href').getall()
        next_page = response.xpath('//div[@class="pages"]/ul/li[last()-1]/a/@href').get()
        next_page_flag = response.xpath('//div[@class="pages"]/ul/li[last()-1]/a/text()').get()
        for title, detail_url in zip(titles, detail_urls):
            item = MeitubacomItem()
            item['title'] = title
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})
        if response.url.split('/')[-1] is not next_page and next_page_flag is '下一页':
            new_content = response.urljoin(next_page)
            yield scrapy.Request(new_content, callback=self.parse)

    def parse_detail(self, response):
        '''
        解析详情页
        '''
        item = response.meta['item']
        download_url = response.xpath('//div[@class="photo"]/a/img/@src').getall()
        next_page = response.xpath('//div[@class="pages"]/ul/li[last()]/a/@href').get()
        item['download_url'] = download_url
        yield item
        if next_page is not '#':
            new_url = response.urljoin(next_page)
            yield scrapy.Request(new_url, callback=self.parse_detail, meta={'item': item})



