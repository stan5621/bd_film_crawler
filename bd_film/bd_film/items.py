# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BdFilmItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    film_title = Field()
    film_link = Field()
    film_source = Field()
    film_bd_link = Field()
    film_bd_pass = Field()
    film_360_link = Field()
    film_360_pass = Field()
