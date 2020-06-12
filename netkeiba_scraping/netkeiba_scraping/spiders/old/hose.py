import scrapy
from scrapy_splash import SplashRequest
import re
from urllib.parse import urljoin
from netkeiba_scraping.items import Hose

""" 
    javascriptのレンダリングにsplashを使用しているため、
    sqrapinghub/splashサーバコンテナを立ち上げる必要あり。
    docker container run -d -p 8050:8050 -p 5023:5023 scrapinghub/splash
"""

class HoseSpider(scrapy.Spider):

    name = 'hose'
    allowed_domains = ['race.netkeiba.com', 'db.netkeiba.com']
    
    base_url = 'https://race.netkeiba.com/'

    def __init__(self, date='', *args, **kwargs):

        """ コマンドライン引数として、開催日を受け取る """

        super(HoseSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://race.netkeiba.com/top/race_list.html?kaisai_date=' + date]

    def start_requests(self):

        """ requestをsplashサーバを経由 """

        yield SplashRequest(self.start_urls[0], self.parse, args={'wait': 0.5},)

    def parse(self, response):

        """ 各レースページのリンクをたどる """

        for url in response.css('li.RaceList_DataItem a::attr("href")').re(r'.*/shutuba.html.*'):    
            url_abs = urljoin(self.base_url, url)
            yield response.follow(url_abs, self.parse_races)

    def parse_races(self, response):

        """ 各競走馬のリンクをたどる  """

        for url in response.css('span.HorseName a::attr("href")').getall():
            yield response.follow(url, self.parse_hoses)

    def parse_hoses(self, response):

        """ 競走馬の情報を取得する  """

        hose_id = re.search(r'horse/(\d+)', response.url).group(1)

        # レース結果格納テーブルを取得
        table_rows = response.css('table.db_h_race_results > tbody > tr')

        # 各行のレース情報を取得する
        for row in table_rows:
            race_arr = row.css('td').xpath('string()').getall()

            item = Hose()
            item['hose_id'] = hose_id
            item['race_id'] = re.search(r'race/(\w+)', row.css('td a::attr("href")').getall()[2]).group(1)
            item['gate_num'] = race_arr[7]
            item['hose_num'] = race_arr[8]
            item['odds'] = race_arr[9]
            item['popularity'] = race_arr[10]
            item['rank'] = race_arr[11]
            item['jockey'] = race_arr[12].strip()
            item['burden_weight'] = race_arr[13]
            item['time'] = race_arr[17]
            item['time_diff'] = race_arr[18]
            item['passing_order'] = race_arr[20]
            item['last_3f'] = race_arr[22]
            item['get_prize'] = race_arr[27]

            try:
                item['hose_weight'] = re.search(r'(\d+)\(([+,-]*\d+)\)+' ,race_arr[23]).group(1)
                item['hose_weight_diff'] = re.search(r'(\d+)\(([+,-]*\d+)\)+' ,race_arr[23]).group(2)
            except AttributeError:
                # 空白の場合エラーとなるのでこちらを使用
                item['hose_weight'] = ''
                item['hose_weight_diff'] = ''

            yield item