import scrapy
from urllib.parse import urljoin
from netkeiba_scraping.spiders.module.parse_module import ParseModuleSpider
import re

""" 
    レースページ
    　　-> 各競走馬ページ
    　　　  -> 過去レース結果情報を取得しDB保存する

    start_urls の例：https://race.netkeiba.com/race/shutuba.html?race_id=202005030411
"""

class RaceSpider(scrapy.Spider):

    name = 'race'
    allowed_domains = ['race.netkeiba.com', 'db.netkeiba.com']
    start_urls = ['https://race.netkeiba.com/race/shutuba.html?race_id=202005030611']
    base_url = 'https://db.netkeiba.com/'

    def parse(self, response):

        """
            以下の処理を行う。
            1. 出馬表基本情報の取得
            2. 出馬表-競走馬情報の取得
            3. 各競走馬のリンクをたどる
         """

        # 1. レース基本情報の取得
        yield ParseModuleSpider.parse_race(self, response)

        hose_links = response.css('span.HorseName > a::attr("href")').getall()

        # 2. 出馬表-競走馬情報の取得
        race_id = re.search(r'race_id=(\d+)', response.url).group(1)
        for hose in hose_links:
            yield ParseModuleSpider.parse_race_hose(self, race_id, hose)

        # 3.各競走馬データのリンクをたどる
        for hose_link in hose_links:
            yield response.follow(hose_link, self.parse_second)

    def parse_second(self, response):

        """ 競走馬ページより以下の処理を行う
            1. 競走馬基本データを取得する
            2. 各馬成績を取得する
            3. レース結果のリンクをたどる
        """

        # 1. 競走馬基本データ
        hose_id = re.search(r'horse/(\d+)', response.url).group(1)
        table_rows = response.css('table.db_h_race_results > tbody > tr')
        yield ParseModuleSpider.parse_hose(self, hose_id, response)

        # 2. 各馬成績
        for race in table_rows:
            yield ParseModuleSpider.parse_race_result_by_hose(self, hose_id, race)

        # 3. レース結果
        for race in table_rows:
            url_abs = urljoin(self.base_url, race.css('a::attr("href")').getall()[2])
            yield response.follow(url_abs, self.parse_third)

    def parse_third(self, response):

        """ レースの結果を取得する """

        yield ParseModuleSpider.parse_race_result(self, response)