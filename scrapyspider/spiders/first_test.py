# -*- coding: utf-8 -*-

'''scrapy入门例子'''
import scrapy

class First_Test(scrapy.Spider):
    name = 'first_test'
    start_urls = ['https://woodenrobot.me']

    def parse(self, response):
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            print title.strip()