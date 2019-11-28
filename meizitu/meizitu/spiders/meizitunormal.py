# -*- coding: utf-8 -*-
import scrapy


class MeizitunormalSpider(scrapy.Spider):
    name = 'meizitunormal'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/all/']

    def parse(self, response):
        years = response.xpath('//div[@class="year"]')
        for year in years:
            rawmonth = year.xpath('./following-sibling::ul[1]//li/p[1]')
            months = rawmonth.xpath('./em/text()').getall()
            print(months)
            for month in months:
                reallink = rawmonth.xpath('./following-sibling::p[1]/a/@href').getall()
                rawname = rawmonth.xpath('./following-sibling::p[1]/a/text()').getall()
                realyear = year.xpath('./text()').get()
                for name, url in zip(rawname, reallink):
                    realname = month + ":" + name
                    print(realname)
                    print(url)
            print(realyear)

