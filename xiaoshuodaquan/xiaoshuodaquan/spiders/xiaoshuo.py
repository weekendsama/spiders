# -*- coding: utf-8 -*-
import scrapy


class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo'
    allowed_domains = ['xiaoshuodaquan.com']
    start_urls = ['https://www.xiaoshuodaquan.com/xuanhuan/']

    def parse(self, response):
        book_urls = response.xpath('//ul[@class="clearfix"]/li/span[2]/a[1]/@href').getall()
        book_names = response.xpath('//ul[@class="clearfix"]/li/span[2]/a[1]/text()').getall()
        for urls, names in zip(book_urls, book_names):

