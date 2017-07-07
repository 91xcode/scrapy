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