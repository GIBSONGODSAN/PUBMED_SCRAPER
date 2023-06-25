# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WikiscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PubItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    citation = scrapy.Field()
    pmid = scrapy.Field()
    free = scrapy.Field()
    review = scrapy.Field()
