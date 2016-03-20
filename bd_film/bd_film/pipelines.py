# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb

import settings


class BdFilmPipeline(object):

    def __init__(self):
         self.db_host = settings.DB_HOST,
         self.db_user = settings.DB_USER,
         self.db_passwd = settings.DB_PASSWD,
         self.db_name = settings.DB_NAME,
         self.db_port = settings.DB_PORT,
         self.db_charset = settings.DB_CHARSET

    def open_spider(self, spider):
         self.conn=MySQLdb.connect(host=self.db_host[0], user=self.db_user[0],
                                   passwd=self.db_passwd[0], db=self.db_name[0],
                                   port=self.db_port[0] , charset=self.db_charset)
         self.cur=self.conn.cursor() 
   
    def close_spider(self, spider):
         self.cur.close() 
         self.conn.close()

    def process_item(self, item, spider):
        insert_film_sql = "insert into film(film_title, film_link, film_source, film_bd_link, film_bd_pass, film_360_link, film_360_pass) values('%s','%s','%s','%s','%s','%s','%s')" % (item['film_title'],item['film_link'], item['film_source'], item['film_bd_link'], item['film_bd_pass'], item['film_360_link'], item['film_360_pass'])
        insert_tv_sql = "insert into tv(tv_title, tv_link, tv_source, tv_bd_link, tv_bd_pass, tv_360_link, tv_360_pass) values('%s','%s','%s','%s','%s','%s','%s')" % (item['film_title'],item['film_link'], item['film_source'], item['film_bd_link'], item['film_bd_pass'], item['film_360_link'], item['film_360_pass'])

        if spider.name == 'film_spider' or spider.name == 'tt_film_spider':
            self.cur.execute(insert_film_sql)
            self.conn.commit()
        elif spider.name == 'film_incr_spider' or spider.name == 'tt_film_incr_spider':
            count = self.cur.execute("select * from film where film_source='%s'" % item['film_source'])
            if count == 0:
                self.cur.execute(insert_film_sql)
                self.conn.commit()
        elif spider.name == 'tv_spider':
            self.cur.execute(insert_tv_sql)
            self.conn.commit()
        elif spider.name == 'tv_incr_spider':
            count = self.cur.execute("select * from tv where tv_title='%s'" % item['film_title'])
            if count == 0:
                self.cur.execute(insert_tv_sql)
                self.conn.commit()
