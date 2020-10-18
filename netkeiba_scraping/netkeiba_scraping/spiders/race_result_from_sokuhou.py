"""
    レース結果ページ単体からレース結果を取得を取得するためのSpider
    start_urls の例: https://db.netkeiba.com/race/202008010111/
"""

import scrapy
from scrapy.spiders import Rule
from netkeiba_scraping.spiders.module.parse_module import ParseModuleSpider
from datetime import datetime, timedelta
from netkeiba_scraping.spiders.module.urlGenerator import getUrls

class RaceResultSpider(scrapy.Spider):

    name = 'race_result_from_sokuhou'
    allowed_domains = ['race.netkeiba.com']

    start_urls = ['https://race.netkeiba.com/race/result.html?race_id=202002020611']

    def parse(self, response):
       yield ParseModuleSpider.parse_race_result_from_sokuhou(self, response)