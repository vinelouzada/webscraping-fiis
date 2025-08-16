# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FiisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class InfoMoneyItem(scrapy.Item):
    fii = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    created_at = scrapy.Field()

class FIIsNoticiasItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    published_at = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    created_at = scrapy.Field()