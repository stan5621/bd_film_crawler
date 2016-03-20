# -*- coding: utf-8 -*-
import re

from scrapy.http import Request
from scrapy.selector import Selector
import scrapy

from bd_film.items import BdFilmItem


class TVSpider(scrapy.Spider):
    name = "tv_spider"
    allowed_domains = ["loldytt.com"]
    start_urls = (
        'http://www.loldytt.com/Dianshiju/chart/1.html',
        'http://www.loldytt.com/Zuixinmeiju/chart/1.html',
        'http://www.loldytt.com/Zuixinhanju/chart/1.html',
        'http://www.loldytt.com/Zuixingangju/chart/1.html',
        'http://www.loldytt.com/Ouxiangju/chart/1.html',
        'http://www.loldytt.com/Zuixinriju/chart/1.html',
        'http://www.loldytt.com/Taiguodianshiju/chart/1.html'
    )

    def parse(self, response):
        page_list = response.selector.xpath('//div//a[re:test(@href, "chart/\d+.html")]//@href').extract()
        page_num_list = [ int(re.findall('chart/(\d+).html', page)[0]) for page in page_list]
        max_page_num = max(page_num_list)
        base_url = re.findall('(.*)/chart/1.html$', response.url)[0]
        for page_num in range(1, max_page_num+1):
            next_page_url = '{}/chart/{}.html'.format(base_url, page_num)
            yield Request(url = next_page_url, method = 'get', callback = self.parse_pageitem)

    def parse_pageitem(self, response):       
        film_url_list = response.selector.xpath('//div//li//div//a[re:test(@href, "http://www.loldytt.com.*")]/@href').extract()
        for film_url in film_url_list:
            yield Request(url = film_url, method = 'get', callback = self.parse_tv)

    def parse_tv(self, response):
        sel = response.selector
        film_360_link = None
        film_360_pass = None
        film_bd_link = None
        film_bd_pass = None
        xl_film = response.selector.xpath('//ul[contains(@class, "downurl")]//li/a')
        for xl in xl_film:
            film_title = xl.xpath('text()')[0].extract()
            film_link = xl.xpath('@href')[0].extract()
            
            item = BdFilmItem()
            item['film_title'] = film_title
            item['film_link'] = film_link
            item['film_360_link'] = film_360_link
            item['film_360_pass'] = film_360_pass
            item['film_bd_link'] = film_bd_link
            item['film_bd_pass'] = film_bd_pass
            item['film_source'] = response.url
            yield item


class TVIncrSpider(scrapy.Spider):
    name = "tv_incr_spider"
    allowed_domains = ["loldytt.com"]
    start_urls = (
        'http://www.loldytt.com/Dianshiju/chart/1.html',
        'http://www.loldytt.com/Zuixinmeiju/chart/1.html',
        'http://www.loldytt.com/Zuixinhanju/chart/1.html',
        'http://www.loldytt.com/Zuixingangju/chart/1.html',
        'http://www.loldytt.com/Ouxiangju/chart/1.html',
        'http://www.loldytt.com/Zuixinriju/chart/1.html',
        'http://www.loldytt.com/Taiguodianshiju/chart/1.html'
    )


    def parse(self, response):
        film_url_list = response.selector.xpath('//div//li//div//a[re:test(@href, "http://www.loldytt.com.*")]/@href').extract()
        for film_url in film_url_list:
            yield Request(url = film_url, method = 'get', callback = self.parse_tv)

    def parse_tv(self, response):
        sel = response.selector
        film_360_link = None
        film_360_pass = None
        film_bd_link = None
        film_bd_pass = None
        xl_film = response.selector.xpath('//ul[contains(@class, "downurl")]//li/a')
        for xl in xl_film:
            film_title = xl.xpath('text()')[0].extract()
            film_link = xl.xpath('@href')[0].extract()

            item = BdFilmItem()
            item['film_title'] = film_title
            item['film_link'] = film_link
            item['film_360_link'] = film_360_link
            item['film_360_pass'] = film_360_pass
            item['film_bd_link'] = film_bd_link
            item['film_bd_pass'] = film_bd_pass
            item['film_source'] = response.url
            yield item

