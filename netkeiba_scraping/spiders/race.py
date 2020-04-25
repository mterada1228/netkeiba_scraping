import scrapy
from scrapy_splash import SplashRequest
import re
from urllib.parse import urljoin

""" 
    javascriptのレンダリングにsplashを使用しているため、
    sqrapinghub/splashサーバコンテナを立ち上げる必要あり。
"""

class RaceSpider(scrapy.Spider):

    name = 'race'
    allowed_domains = ['race.netkeiba.com']
    
    base_url = 'https://race.netkeiba.com/'

    def __init__(self, date='', *args, **kwargs):

        """ コマンドライン引数として、開催日を受け取る """

        super(RaceSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://race.netkeiba.com/top/race_list.html?kaisai_date=' + date]

    def start_requests(self):

        """ requestをsplashサーバを経由 """

        yield SplashRequest(self.start_urls[0], self.parse, args={'wait': 0.5},)

    def parse(self, response):

        for url in response.css('li.RaceList_DataItem a::attr("href")').re(r'.*/shutuba.html.*'):
            
            url_abs = urljoin(self.base_url, url)

            yield response.follow(url_abs, self.parse_races)

    def parse_races(self, response):

        print(response.css('title'))