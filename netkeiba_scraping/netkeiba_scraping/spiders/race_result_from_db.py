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

    name = 'race_result_from_db'
    allowed_domains = ['db.netkeiba.com']

    base_url = 'https://db.netkeiba.com/race/'

    """ 
        競馬場コード
        43: 船橋
    """
    cource_code = '43'

    # 検索開始、終了日
    start_date = datetime(2017, 6, 17)
    end_date = datetime(2020, 6, 17)

    # start_urls = getUrls(base_url, cource_code, start_date, end_date, query='/')
    start_urls = ['https://db.netkeiba.com/race/201908040411/',
                  'https://db.netkeiba.com/race/201808040511/',
                  'https://db.netkeiba.com/race/201708040511/',
                  'https://db.netkeiba.com/race/201608040511/',
                  'https://db.netkeiba.com/race/201508040511/',
                  '',
                  ''
                  ]

    def parse(self, response):

       # 存在しないレースのURLはコンテンツが空のページが表示されるので、チェックしてスキップする。
       if response.css('div.mainrace_data > div.data_intro') == []:
           return

       yield ParseModuleSpider.parse_race_result(self, response)