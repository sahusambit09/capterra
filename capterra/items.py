# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CapterraItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    slug = scrapy.Field()
    api_url = scrapy.Field()
    site_id = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    image = scrapy.Field()
    review = scrapy.Field()
    feature = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    created_date = scrapy.Field()
