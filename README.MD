```
Scrapy新手教程
    Python 2.7.6
    Scrapy (0.24.4)
    
```

```
第一步:创建项目
scrapy startproject scrapyspider
该命令将会创建包含下列内容的scrapyspider目录:

scrapyspider/
    scrapy.cfg
    scrapyspider/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...
这些文件分别是:

scrapy.cfg: 项目的配置文件。
scrapyspider/: 该项目的python模块。之后您将在此加入代码。
scrapyspider/items.py: 项目中的item文件。
scrapyspider/pipelines.py: 项目中的pipelines文件。
scrapyspider/settings.py: 项目的设置文件。
scrapyspider/spiders/: 放置spider代码的目录。
编写第一个爬虫(Spider)

Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。

其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 item 的方法。

为了创建一个Spider，您必须继承 scrapy.Spider 类， 且定义以下三个属性:

name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
start_urls: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。
以下为我们的第一个Spider代码，保存在scrapyspider/spiders目录下的first_spider.py文件中:


# -*- coding: utf-8 -*-


import scrapy

class BlogSpider(scrapy.Spider):
    name = 'first_test'
    start_urls = ['https://woodenrobot.me']

    def parse(self, response):
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            print title.strip()
            
            
```

```
   
进入项目目录,执行下面
scrapy crawl first_test

会看到如下信息:

2017-07-07 18:55:00+0800 [scrapy] INFO: Scrapy 0.24.4 started (bot: scrapyspider)
2017-07-07 18:55:00+0800 [scrapy] INFO: Optional features available: ssl, http11
2017-07-07 18:55:00+0800 [scrapy] INFO: Overridden settings: {'NEWSPIDER_MODULE': 'scrapyspider.spiders', 'SPIDER_MODULES': ['scrapyspider.spiders'], 'BOT_NAME': 'scrapyspider'}
2017-07-07 18:55:00+0800 [scrapy] INFO: Enabled extensions: LogStats, TelnetConsole, CloseSpider, WebService, CoreStats, SpiderState
2017-07-07 18:55:00+0800 [scrapy] INFO: Enabled downloader middlewares: HttpAuthMiddleware, DownloadTimeoutMiddleware, UserAgentMiddleware, RetryMiddleware, DefaultHeadersMiddleware, MetaRefreshMiddleware, HttpCompressionMiddleware, RedirectMiddleware, CookiesMiddleware, ChunkedTransferMiddleware, DownloaderStats
2017-07-07 18:55:00+0800 [scrapy] INFO: Enabled spider middlewares: HttpErrorMiddleware, OffsiteMiddleware, RefererMiddleware, UrlLengthMiddleware, DepthMiddleware
2017-07-07 18:55:00+0800 [scrapy] INFO: Enabled item pipelines: 
2017-07-07 18:55:00+0800 [woodenrobot] INFO: Spider opened
2017-07-07 18:55:00+0800 [woodenrobot] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2017-07-07 18:55:00+0800 [scrapy] DEBUG: Telnet console listening on 127.0.0.1:6023
2017-07-07 18:55:00+0800 [scrapy] DEBUG: Web service listening on 127.0.0.1:6080
2017-07-07 18:55:01+0800 [woodenrobot] DEBUG: Crawled (200) <GET https://woodenrobot.me> (referer: None)
ssh-keygen详解
用Sphinx快速制作文档
Scrapy爬虫框架教程（四）-- 抓取AJAX异步加载网页
Scrapy爬虫框架教程（三）-- 调试(Debugging)Spiders
利用爬虫和树莓派3打造自己的语音天气闹钟
Scrapy爬虫框架教程（二）-- 爬取豆瓣电影TOP250
scrapy爬虫框架教程（一）-- Scrapy入门
波浪起伏的2016年
用BeautifulSoup库抓取信息时去掉字符串首尾空白的几种方法
Python中os.path.dirname(__file__)的用法
2017-07-07 18:55:01+0800 [woodenrobot] INFO: Closing spider (finished)
2017-07-07 18:55:01+0800 [woodenrobot] INFO: Dumping Scrapy stats:
	{'downloader/request_bytes': 213,
	 'downloader/request_count': 1,
	 'downloader/request_method_count/GET': 1,
	 'downloader/response_bytes': 10432,
	 'downloader/response_count': 1,
	 'downloader/response_status_count/200': 1,
	 'finish_reason': 'finished',
	 'finish_time': datetime.datetime(2017, 7, 7, 10, 55, 1, 605728),
	 'log_count/DEBUG': 3,
	 'log_count/INFO': 7,
	 'response_received_count': 1,
	 'scheduler/dequeued': 1,
	 'scheduler/dequeued/memory': 1,
	 'scheduler/enqueued': 1,
	 'scheduler/enqueued/memory': 1,
	 'start_time': datetime.datetime(2017, 7, 7, 10, 55, 0, 813369)}
2017-07-07 18:55:01+0800 [woodenrobot] INFO: Spider closed (finished)
```


```
第二步:Scrapy爬虫框架教程-- 爬取豆瓣电影TOP250

编辑上面的目录 items.py 文件

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()
    # 封面
    img = scrapy.Field()
 
新建文件douban_web_spider.py 在scrapyspider/spiders目录下:
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
```


```
进入项目目录,执行下面
scrapy crawl douban_movie_top250
会看到
2017-07-07 19:09:57+0800 [douban_movie_top250] DEBUG: Scraped from <200 https://movie.douban.com/top250?start=225&filter=>
	{'movie_name': u'\u5f57\u661f\u6765\u7684\u90a3\u4e00\u591c',
	 'ranking': u'248',
	 'score': u'8.3',
	 'score_num': u'150809'}
2017-07-07 19:09:57+0800 [douban_movie_top250] DEBUG: Scraped from <200 https://movie.douban.com/top250?start=225&filter=>
	{'movie_name': u'\u9ed1\u9e70\u5760\u843d',
	 'ranking': u'249',
	 'score': u'8.5',
	 'score_num': u'101666'}
2017-07-07 19:09:57+0800 [douban_movie_top250] DEBUG: Scraped from <200 https://movie.douban.com/top250?start=225&filter=>
	{'movie_name': u'\u5047\u5982\u7231\u6709\u5929\u610f',
	 'ranking': u'250',
	 'score': u'8.2',
	 'score_num': u'217235'}
2017-07-07 19:09:57+0800 [douban_movie_top250] INFO: Closing spider (finished)
2017-07-07 19:09:57+0800 [douban_movie_top250] INFO: Dumping Scrapy stats:
	{'downloader/request_bytes': 3913,
	 'downloader/request_count': 10,
	 'downloader/request_method_count/GET': 10,
	 'downloader/response_bytes': 127359,
	 'downloader/response_count': 10,
	 'downloader/response_status_count/200': 10,
	 'finish_reason': 'finished',
	 'finish_time': datetime.datetime(2017, 7, 7, 11, 9, 57, 313346),
	 'item_scraped_count': 250,
	 'log_count/DEBUG': 262,
	 'log_count/INFO': 7,
	 'request_depth_max': 9,
	 'response_received_count': 10,
	 'scheduler/dequeued': 10,
	 'scheduler/dequeued/memory': 10,
	 'scheduler/enqueued': 10,
	 'scheduler/enqueued/memory': 10,
	 'start_time': datetime.datetime(2017, 7, 7, 11, 9, 55, 405693)}
2017-07-07 19:09:57+0800 [douban_movie_top250] INFO: Spider closed (finished)
```


```
将爬取的数据写到数据库中

先建一张表:
    CREATE TABLE `liu`.`doubanmoive` (
        `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
        `movie_name` varchar(255) DEFAULT '',
        `ranking` varchar(255),
        `score` varchar(255),
        `score_num` varchar(255),
        `img` text,
        PRIMARY KEY (`id`)
    ) DEFAULT CHARACTER SET utf8 COMMENT=''

然后修改pipelines.py

    # -*- coding: utf-8 -*-
    
    # Define your item pipelines here
    #
    # Don't forget to add your pipeline to the ITEM_PIPELINES setting
    # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
    
    
    #class DoubanmoivePipeline(object):
    #    def process_item(self, item, spider):
    #        return item
    
    import json
    import codecs
    
    from scrapy import log
    from twisted.enterprise import adbapi
    from scrapy.http import Request
    
    import urllib
    import MySQLdb
    import MySQLdb.cursors
    
    
    class ScrapyspiderPipeline(object):
        def process_item(self, item, spider):
            return item
    
    '''保存文件'''
    class SavePipeline(object):
        def __init__(self):
            self.file = codecs.open('save_data.json', mode='wb', encoding='utf-8')
    
        def process_item(self, item, spider):
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape"))
            return item
    
    '''数据写到数据库'''
    class DoPipeline(object):
        def __init__(self):
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                    db = 'liu',
                    user = 'root',
                    passwd = '',
                    cursorclass = MySQLdb.cursors.DictCursor,
                    charset = 'utf8',
                    use_unicode = False
            )
        def process_item(self, item, spider):
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    
        def _conditional_insert(self,tx,item):
            tx.execute("select * from doubanmoive where ranking= %s",(item['ranking']))
            result=tx.fetchone()
            log.msg("result", level='INFO')
            print result
            if result:
                log.msg("Item already stored in db:%s" % item, level='INFO')
            else:
    
                #获取海报下载地址
                site= item['img']           #截取海报地址的最后一个/,生成本地的文件名
                str = site.split('/');
                print str
                path = str[-1]
                print 'local img path %s'%(path)
                #开始下载海报
                print '--------------------download img %s'%(site)
                data = urllib.urlopen(site).read()
                newfile = open(path,"wb")
                newfile.write(data)
                newfile.close()
                tx.execute(\
                    "insert into doubanmoive (movie_name,ranking,score,score_num,img) values (%s,%s,%s,%s,%s)",\
                     ("".join(item['movie_name']), "".join(item['ranking']), "".join(item['score']), "".join(item['score_num']), "".join(item['img'])))
                log.msg("Item stored in db: %s" % item, level='INFO')
        def handle_error(self, e):
            log.err(e)
    
        
然后 修改settings.py
    # -*- coding: utf-8 -*-
    
    # Scrapy settings for scrapyspider project
    #
    # For simplicity, this file contains only the most important settings by
    # default. All the other settings are documented here:
    #
    #     http://doc.scrapy.org/en/latest/topics/settings.html
    #
    
    BOT_NAME = 'scrapyspider'
    
    SPIDER_MODULES = ['scrapyspider.spiders']
    NEWSPIDER_MODULE = 'scrapyspider.spiders'
    
    
    ITEM_PIPELINES={
        'scrapyspider.pipelines.DoPipeline':300,
    }
    
    # Crawl responsibly by identifying yourself (and your website) on the user-agent
    #USER_AGENT = 'scrapyspider (+http://www.yourdomain.com)'


```

```
然后执行 scrapy crawl douban_movie_top250
```