import scrapy
from urllib.parse import urljoin
from netkeiba_scraping.spiders.module.parse_module import ParseModuleSpider

""" 
    レースページ
    　　-> 各競走馬ページ
    　　　  -> 過去レース結果情報を取得しDB保存する

    start_urls の例：https://race.netkeiba.com/race/shutuba.html?race_id=202005030411
"""

class RaceSpider(scrapy.Spider):

    name = 'race'
    allowed_domains = ['race.netkeiba.com, db.netkeiba.com']
    start_urls = ['https://race.netkeiba.com/race/shutuba.html?race_id=202005030411']
    base_url = 'https://race.netkeiba.com/'

    def parse(self, response):

        """ レース基本情報の取得 """

        yield ParseModuleSpider.parse_race(self, response)
