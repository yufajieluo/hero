# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyAudltItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    create_time = scrapy.Field()
    content = scrapy.Field()

class PictureItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    create_time = scrapy.Field()
    urls = scrapy.Field()
    paths = scrapy.Field()

