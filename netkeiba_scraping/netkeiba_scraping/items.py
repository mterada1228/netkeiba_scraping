# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Race(scrapy.Item):

    """ レース情報  """

    race_id = scrapy.Field()
    race_date = scrapy.Field()
    race_cource = scrapy.Field()
    round = scrapy.Field()
    race_name = scrapy.Field()
    grade = scrapy.Field()
    start_time = scrapy.Field()
    cource_type = scrapy.Field()
    distance = scrapy.Field()
    turn = scrapy.Field()
    side = scrapy.Field()
    days = scrapy.Field()
    regulation1 = scrapy.Field()
    regulation2 = scrapy.Field()
    regulation3 = scrapy.Field()
    regulation4 = scrapy.Field()
    prize1 = scrapy.Field()
    prize2 = scrapy.Field()
    prize3 = scrapy.Field()
    prize4 = scrapy.Field()
    prize5 = scrapy.Field()

class RaceResult(scrapy.Item):

    """ レース結果 """
    
    id = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    condition = scrapy.Field()
    entire_rap = scrapy.Field()
    ave_1F = scrapy.Field()
    first_half_ave_3F = scrapy.Field()
    last_half_ave_3F = scrapy.Field()
    RPCI = scrapy.Field()

class HoseRaceResult(scrapy.Item):

    """ 競走馬-レース情報 """

    hose_id = scrapy.Field()
    race_id = scrapy.Field()
    gate_num = scrapy.Field()
    hose_num = scrapy.Field()
    odds = scrapy.Field()
    popularity = scrapy.Field()
    rank = scrapy.Field()
    jockey = scrapy.Field()
    burden_weight = scrapy.Field()
    time = scrapy.Field()
    time_diff = scrapy.Field()
    passing_order = scrapy.Field()
    last_3f = scrapy.Field()
    hose_weight = scrapy.Field()
    hose_weight_diff = scrapy.Field()
    get_prize = scrapy.Field()

class Hose(scrapy.Item):

    """ 競走馬基本情報 """

    hose_id = scrapy.Field()
    name = scrapy.Field()