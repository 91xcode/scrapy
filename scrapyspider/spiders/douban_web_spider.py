# -*- coding: utf-8 -*-



import scrapy
from scrapyspider.items import DoubanMovieItem
from scrapy import log
from scrapy import Request


class DoubanMovieTop250Spider(scrapy.Spider):
    name = 'douban_movie_top250'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item = DoubanMovieItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="star"]/span/text()').re(ur'(\d+)人评价')[0]
            item['img'] = movie.xpath(
                '//*[@class="pic"]/a/img/@src').extract()[0]

            yield item

            log.msg("Appending item...", level='INFO')

        log.msg("Append done.", level='INFO')



        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:

            next_url = 'https://movie.douban.com/top250' + next_url[0]
            log.msg("Start Get next_url,next_url:%s" % next_url, level='INFO')
            yield Request(next_url, headers=self.headers)