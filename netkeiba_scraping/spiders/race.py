import scrapy
from scrapy_splash import SplashRequest
import re
from urllib.parse import urljoin
from netkeiba_scraping.items import Race

""" 
    javascriptのレンダリングにsplashを使用しているため、
    sqrapinghub/splashサーバコンテナを立ち上げる必要あり。
    docker container run -d -p 8050:8050 -p 5023:5023 scrapinghub/splash
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

        """ 各レースページのリンクをたどる """

        for url in response.css('li.RaceList_DataItem a::attr("href")').re(r'.*/shutuba.html.*'):
            
            url_abs = urljoin(self.base_url, url)

            yield response.follow(url_abs, self.parse_races)

    def parse_races(self, response):

        """ レース情報を取得する  """

        # 例) 15:40発走 / 芝1600m (左)
        RaceData01 = response.css('div.RaceData01').xpath('string()').get().split('\n')[1]
        # 例) ['', '2回', '東京', '6日目', 'サラ系３歳', 'オープン', '\xa0\xa0\xa0\xa0\xa0', '(国際) 牡・牝(指)', '定量', '22頭', '', '本賞金:10500,4200,2600,1600,1050万円', '']
        RaceData02 = response.css('div.RaceData02').xpath('string()').get().split('\n')
        prizes = re.findall(r'\d+', RaceData02[11])
        
        item = Race()
        item['race_cource'] = RaceData02[2]
        item['round'] = response.css('span.RaceNum')[0].xpath('string()').get()
        item['race_name'] = response.css('div.RaceName').xpath('string()').get().strip()
        item['grade'] = re.search(r'class=.*\s(\w+)', response.css('div.RaceName > span.Icon_GradeType').get()).group(1)
        item['distance'] = re.search(r'(\d+)m', RaceData01).group(1)
        item['turn'] = re.search(r'\((\D+)\)', RaceData01).group(1).split(' ')[0]
        item['days'] = RaceData02[3]
        item['regulation1'] = RaceData02[4]
        item['regulation2'] = RaceData02[5]
        item['regulation3'] = RaceData02[7]
        item['regulation4'] = RaceData02[8]
        item['prize1'] = prizes[0]
        item['prize2'] = prizes[1]
        item['prize3'] = prizes[2]
        item['prize4'] = prizes[3]
        item['prize5'] = prizes[4]

        try:
            item['side'] = re.search(r'\((\D+)\)', RaceData01).group(1).split(' ')[1]
        except IndexError:
            # 内回り、外回りの存在しないコースではエラーとなるので、こちらを使用
            item['side'] = ''

        try:
            item['start_time'] = re.search(r'(.*)発走', RaceData01).group(1)
        except AttributeError:
            # 発走時間が未定の場合はエラーとなるので、こちらを使用
            item['start_time'] = ''

        try:
            item['cource_type'] = re.search(r'/\s(\D*)(\d*)', RaceData01).group(1)
        except AttributeError:
            # 発走時間が未定の場合はエラーとなるので、こちらを使用
            re.search(r'\s(\D+)', RaceData01).group(1)

        yield item
        