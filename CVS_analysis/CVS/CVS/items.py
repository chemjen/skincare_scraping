# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CvsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	name = scrapy.Field()
	brand = scrapy.Field()
	genus = scrapy.Field()
	family = scrapy.Field()
	species = scrapy.Field()
	details = scrapy.Field()
	url = scrapy.Field()
	price = scrapy.Field()
	ounces = scrapy.Field()
	pounds = scrapy.Field()
	ave_rating = scrapy.Field()
	num_reviews = scrapy.Field()

