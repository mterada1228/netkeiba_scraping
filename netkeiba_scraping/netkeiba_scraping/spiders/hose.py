""" 
    競争馬ページからレース結果と各馬成績を取得を取得するためのSpider
    start_urls の例: https://db.netkeiba.com/horse/2014105558/
"""

import scrapy
from urllib.parse import urljoin
from netkeiba_scraping.items import HoseRaceResult
from netkeiba_scraping.spiders.module.parse_module import ParseModuleSpider
import re

class HoseSpider(scrapy.Spider):

    name = 'hose'
    allowed_domains = ['race.netkeiba.com', 'db.netkeiba.com']
    start_urls = ['https://db.netkeiba.com/horse/2015104126']

    base_url = 'https://db.netkeiba.com/'

    def parse(self, response):

        """ 各レース結果ページのリンクをたどる """

        hose_id = re.search(r'horse/(\d+)', response.url).group(1)
        table_rows = response.css('table.db_h_race_results > tbody > tr')

        # 各馬成績を取得する
        for race in table_rows:
            yield ParseModuleSpider.parse_race_result_by_hose(self, hose_id, race)

        # レース結果を取得する
        for race in table_rows:
            url_abs = urljoin(self.base_url, race.css('a::attr("href")').getall()[2])
            yield response.follow(url_abs, self.parse_second)

    def parse_second(self, response):
        yield ParseModuleSpider.parse_race_result(self, response)