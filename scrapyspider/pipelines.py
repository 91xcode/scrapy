# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from twisted.enterprise import adbapi
from scrapy.http import Request
import MySQLdb
import MySQLdb.cursors
from scrapy import log
import urllib

import copy

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('save.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MySQLStorePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        #深拷贝,防止进入数据库有重复
        asynItem = copy.deepcopy(item)
        d = self.dbpool.runInteraction(self._do_upinsert, asynItem, spider)


        #d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        select_sql =  "select id from doubanmoive where ranking= '%s'"%(item['ranking'])
        conn.execute(select_sql)
        ret = conn.fetchone()

        if ret:
            log.msg("Item already stored in db:%s" % item, level='INFO')
        else:
            self._download_img(item)
            insert_sql = "insert into doubanmoive (movie_name,ranking,score,score_num,img) values ('%s','%s','%s','%s','%s')"\
                         %(item['movie_name'], item['ranking'], item['score'], item['score_num'],item['img'])
            conn.execute(insert_sql)

            log.msg("Item stored in db: %s" % item, level='INFO')


    def _download_img(self,item):
        # 获取海报下载地址
        site = item['img']  # 截取海报地址的最后一个/,生成本地的文件名
        str = site.split('/');
        print str
        path = str[-1]
        print 'local img path %s' % (path)
        # 开始下载海报
        print '--------------------download img %s' % (site)
        data = urllib.urlopen(site).read()
        newfile = open(path, "wb")
        newfile.write(data)
        newfile.close()
        return True

    # 异常处理
    def _handle_error(self, failure, item, spider):
        log.err(failure)
