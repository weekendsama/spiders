# -*- coding: utf-8 -*-
import scrapy
from book365.items import Book365Item

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['365book.net']
    start_urls = ['http://www.365book.net/i-xuanhuan/1']

    def parse(self, response):
        titles = response.xpath('//div[@class="panel-body"]//div/a/img/@alt').getall()
        raw_target_urls = response.xpath('//div[@class="panel-body"]//div/div[@class="bookdesc"]/a/@href').getall()
        raw_next_pager = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').get()
        for title, raw_target_url in zip(titles, raw_target_urls):
            item = Book365Item()
            item['title'] = title
            real_url = raw_target_url.split('/')[-2]
            download_url = r'http://www.365book.net/downLoadfile/{}/'.format(real_url)
            item['download_link'] = download_url
            yield item

        next_pager = raw_next_pager.split('/')[-1]
        if next_pager is not response.url.split('/')[-1]:
            new_page = r'http://www.365book.net/i-xuanhuan/{}'.format(next_pager)
            yield scrapy.Request(new_page, callback=self.parse)

