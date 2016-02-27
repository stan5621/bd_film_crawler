# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

import MySQLdb

class BdFilmPipeline(object):
    
    def process_item(self, item, spider):
        if spider.name == 'film_spider':
            try:
                conn=MySQLdb.connect(host='localhost',user='root',passwd='111111',db='bd_film',port=3306, charset='utf8')
                cur=conn.cursor()
                cur.execute("insert into film(film_title, film_link, film_source, film_bd_link, film_bd_pass, film_360_link, film_360_pass) values('%s','%s','%s','%s','%s','%s','%s')" % (item['film_title'],item['film_link'], item['film_source'], item['film_bd_link'], item['film_bd_pass'], item['film_360_link'], item['film_360_pass']))
                conn.commit()
                cur.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        elif spider.name == 'film_incr_spider':
            try:
                conn=MySQLdb.connect(host='localhost',user='root',passwd='111111',db='bd_film',port=3306, charset='utf8')
                cur=conn.cursor()
                count = cur.execute("select * from film where film_source='%s'" % item['film_source'])
                if count == 0:
                    cur.execute("insert into film(film_title, film_link, film_source, film_bd_link, film_bd_pass, film_360_link, film_360_pass) values('%s','%s','%s','%s','%s','%s','%s')" % (item['film_title'],item['film_link'], item['film_source'], item['film_bd_link'], item['film_bd_pass'], item['film_360_link'], item['film_360_pass']))
                    conn.commit()
                cur.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
