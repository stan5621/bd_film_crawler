# -*- coding: utf-8 -*-
import re

from scrapy.selector import Selector
from scrapy.http import Request
import scrapy

from bd_film.items import BdFilmItem


class FilmSpiderSpider(scrapy.Spider):
    name = "film_spider"
    allowed_domains = ["bd-film.com"]
    start_urls = (
        'http://www.bd-film.com/zx/index.htm',
        'http://www.bd-film.com/gq/index.htm',
        'http://www.bd-film.com/gy/index.htm',
        'http://www.bd-film.com/zy/index.htm',
        'http://www.bd-film.com/jd/index.htm',
        'http://www.bd-film.com/dh/index.htm'
    )

    def parse(self, response):
        page_list = response.selector.xpath('//li//a[re:test(@href, "index_\d+.htm")]//@href').extract()
        page_num_list = [ int(re.findall('index_(\d+).htm', page)[0]) for page in page_list]
        max_page_num = max(page_num_list)
        base_url = re.findall('(.*)/index.htm$', response.url)[0]
        for page_num in range(1, max_page_num+1):
            next_page_url = '{}/index_{}.htm'.format(base_url, page_num)
            yield Request(url = next_page_url, method = 'get', callback = self.parse_pageitem)

    def parse_pageitem(self, response):       
        film_url_list = response.selector.xpath('//tr//a[re:test(@href, "http://www.bd-film.com.*\d+.htm")]/@href').extract()
        for film_url in film_url_list:
            yield Request(url = film_url, method = 'get', callback = self.parse_film)

    def parse_film(self, response):
        sel = response.selector
        film_360_link = None
        film_360_pass = None
        film_bd_link = None
        film_bd_pass = None
        film_title = sel.xpath('//h3/text()').extract()[0]
        film_link = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@id, "xl_link")]//@onclick').re(r"xldown\(\'(.*)(\r|\'\))")[0]
        film_360_link_list = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "yunpan")]//@href').extract()
        if len(film_360_link_list) != 0:
            film_360_link = film_360_link_list[0]
            film_360_pass = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "yunpan")]//text()').re(u".*\u5bc6\u7801\uff1a(.*)\)")[0]
        film_bd_link_list = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "pan.baidu")]//@href').extract()
        if len(film_bd_link_list) != 0:
            film_bd_link = film_bd_link_list[0]
            film_bd_pass = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "pan.baidu")]//text()').re(u".*\u5bc6\u7801\uff1a(.*)\)")[0]
        item = BdFilmItem()
        item['film_title'] = film_title
        item['film_link'] = film_link
        item['film_360_link'] = film_360_link
        item['film_360_pass'] = film_360_pass
        item['film_bd_link'] = film_bd_link
        item['film_bd_pass'] = film_bd_pass
        item['film_source'] = response.url
        yield item

class FilmSpiderIncrSpider(scrapy.Spider):
    name = "film_incr_spider"
    allowed_domains = ["bd-film.com"]
    start_urls = (
        'http://www.bd-film.com/zx/index.htm',
        'http://www.bd-film.com/gq/index.htm',
        'http://www.bd-film.com/gy/index.htm',
        'http://www.bd-film.com/zy/index.htm',
        'http://www.bd-film.com/jd/index.htm',
        'http://www.bd-film.com/dh/index.htm'
    )

    def parse(self, response):
        film_url_list = response.selector.xpath('//tr//a[re:test(@href, "http://www.bd-film.com.*\d+.htm")]/@href').extract()
        for film_url in film_url_list:
            yield Request(url = film_url, method = 'get', callback = self.parse_film)

    def parse_film(self, response):
        sel = response.selector
        film_360_link = None
        film_360_pass = None
        film_bd_link = None
        film_bd_pass = None
        film_title = sel.xpath('//h3/text()').extract()[0]
        film_link = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@id, "xl_link")]//@onclick').re(r"xldown\(\'(.*)(\r|\'\))")[0]
        film_360_link_list = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "yunpan")]//@href').extract()
        if len(film_360_link_list) != 0:
            film_360_link = film_360_link_list[0]
            film_360_pass = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "yunpan")]//text()').re(u".*\u5bc6\u7801\uff1a(.*)\)")[0]
        film_bd_link_list = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "pan.baidu")]//@href').extract()
        if len(film_bd_link_list) != 0:
            film_bd_link = film_bd_link_list[0]
            film_bd_pass = sel.xpath('//div[contains(@class, "bs-docs-download")]//a[contains(@href, "pan.baidu")]//text()').re(u".*\u5bc6\u7801\uff1a(.*)\)")[0]
        item = BdFilmItem()
        item['film_title'] = film_title
        item['film_link'] = film_link
        item['film_360_link'] = film_360_link
        item['film_360_pass'] = film_360_pass
        item['film_bd_link'] = film_bd_link
        item['film_bd_pass'] = film_bd_pass
        item['film_source'] = response.url
        yield item
