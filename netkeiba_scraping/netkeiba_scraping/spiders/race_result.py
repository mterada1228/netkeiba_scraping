"""
    レース結果ページ単体からレース結果を取得を取得するためのSpider
    start_urls の例: https://db.netkeiba.com/race/202008010111/
"""

import scrapy
from scrapy.spiders import Rule
from netkeiba_scraping.spiders.module.parse_module import ParseModuleSpider
from datetime import datetime, timedelta
import pdb

class RaceResultSpider(scrapy.Spider):

    def getUrls(cource_code, start_date, end_date):

        """ scrapingを実行するurlのリストを返す """

        base_url = 'https://db.netkeiba.com/race/'

        time_diff_days = end_date - start_date + timedelta(days=1)
        time_itereter = timedelta(days=0)

        start_urls = []

        while time_diff_days > time_itereter:
            date = (start_date + time_itereter).strftime('%Y%m%d')
            round_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

            for round in round_list:
                url = base_url + date[0:4] + cource_code + date[4:8] + round + '/'
                start_urls.append(url)
                print(url)

            time_itereter += timedelta(days=1)

        return start_urls

    name = 'race_result'
    allowed_domains = ['db.netkeiba.com']

    """ 
        競馬場コード
        43: 船橋
    """
    cource_code = '43'

    # 検索開始、終了日
    start_date = datetime(2020, 1, 11)
    end_date = datetime(2020, 1, 11)

    start_urls = getUrls(cource_code, start_date, end_date)
    # start_urls = ['https://db.netkeiba.com/race/202045051111/']

    def parse(self, response):

       # 存在しないレースのURLはコンテンツが空のページが表示されるので、チェックしてスキップする。
       if response.css('div.mainrace_data > div.data_intro') == []:
           return

       yield ParseModuleSpider.parse_race_result(self, response)