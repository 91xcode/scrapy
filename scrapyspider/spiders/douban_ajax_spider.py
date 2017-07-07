# -*- coding: utf-8 -*-


import re
import json


from scrapy import Request
import scrapy
from scrapyspider.items import DoubanMovieItem
from scrapy import log


class DoubanAJAXSpider(scrapy.Spider):
    name = 'douban_ajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        datas = json.loads(response.body)
        item = DoubanMovieItem()
        if datas:
            for data in datas:
                item['ranking'] = data['rank']
                item['movie_name'] = data['title']
                item['score'] = data['score']
                item['score_num'] = data['vote_count']
                item['img'] = data['cover_url']
                yield item
                log.msg("Appending item...", level='INFO')

            log.msg("Append done.", level='INFO')
            # 如果datas存在数据则对下一页进行采集
            page_num = re.search(r'start=(\d+)', response.url).group(1)
            page_num = 'start=' + str(int(page_num)+20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            log.msg("Start Get next_url,next_url:%s" % next_url, level='INFO')
            yield Request(next_url, headers=self.headers)
