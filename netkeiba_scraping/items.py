# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class race(scrapy.Item):

    """ レース情報  """

    rece_cource = scrapy.Field()
    round = scrapy.Field()
    race_name = scrapy.Field()
    grade = scrapy.Field()
    start_time = scrapy.Field()
    cource_type = scrapy.Field()
    distance = scrapy.Field()
    turn = scrapy.Field()
    side = scrapy.Field()
    holding_times = scrapy.Field()
    days = scrapy.Field()
    regulation1 = scrapy.Field()
    regulation2 = scrapy.Field()
    special = scrapy.Field()
    prize1 = scrapy.Field()
    prize2 = scrapy.Field()
    prize3 = scrapy.Field()
    prize4 = scrapy.Field()
    prize5 = scrapy.Field()