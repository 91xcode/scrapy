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
    'scrapyspider.pipelines.MySQLStorePipeline':300,
	'scrapyspider.pipelines.JsonWithEncodingPipeline':300,
}


MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'liu'
MYSQL_USER = 'root'
MYSQL_PASSWD = ''

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyspider (+http://www.yourdomain.com)'
