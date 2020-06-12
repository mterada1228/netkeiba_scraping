"""
    最終的に取得したいitemをperseするためのModule
    1. 単体で使うことはできない。
    2. 各Spider はこのClassをimportすること
    3. 永続化するitem を yieldする関数はこちらに記載すること 
"""

import scrapy
import re
from urllib.parse import urljoin
from netkeiba_scraping.items import RaceResult, HoseRaceResult, Hose, Race
from numpy import average

class ParseModuleSpider(scrapy.Spider):

    def parse_race_result(self, response):

        """ レース結果情報を取得 """

        item = RaceResult()

        item['id'] = re.search(r'race/(\d+)/', response.url).group(1)

        data_intro_div = response.css('div.mainrace_data > div.data_intro')        
        mainrace_data_dd = response.css('div.mainrace_data > div.data_intro > dl > dd')       
        small_txt_p_array = data_intro_div.css('p.smalltxt').xpath('string()').get().split(' ')
        mainrace_data_span_array = mainrace_data_dd.css('span').xpath('string()').get().split('\xa0')

        item['name'] = mainrace_data_dd.css('h1').xpath('string()').get() 
        item['date'] = small_txt_p_array[0]
        item['condition'] = mainrace_data_span_array[4]

        race_rap = response.css('td.race_lap_cell').xpath('string()').getall()[0]
        race_rap_float_array = [float(x) for x in race_rap.replace(' ', '').split('-')]
        race_pace = response.css('td.race_lap_cell').xpath('string()').getall()[1]
        race_pace_float_array = [float(x) for x in re.search(r'\(([\d,.,-]+)', race_pace).group(1).split('-')]

        item['entire_rap'] = race_rap.replace(' ', '')
        item['ave_1F'] = average(race_rap_float_array) 
        item['first_half_ave_3F'] = race_pace_float_array[0]
        item['last_half_ave_3F'] = race_pace_float_array[1]
        item['RPCI'] = 50 * race_pace_float_array[0] / race_pace_float_array[1]

        return item

    def parse_race_result_by_hose(self, hose_id, row):

        """ 各馬成績を取得する """

        race_arr = row.css('td').xpath('string()').getall()
        item = HoseRaceResult()
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

        return item

    def parse_hose(self, hose_id, response):

        """ 競走馬基本データを取得する """

        item = Hose()
        item['hose_id'] = hose_id
        item['name'] = response.css('div.horse_title > h1').xpath('string()').get().strip()

        return item

    def parse_race(self, response):

        """ 出馬表基本データを取得する """

        # 例) 15:40発走 / 芝1600m (左)
        RaceData01 = response.css('div.RaceData01').xpath('string()').get().split('\n')[1]
        # 例) ['', '2回', '東京', '6日目', 'サラ系３歳', 'オープン', '\xa0\xa0\xa0\xa0\xa0', '(国際) 牡・牝(指)', '定量', '22頭', '', '本賞金:10500,4200,2600,1600,1050万円', '']
        RaceData02 = response.css('div.RaceData02').xpath('string()').get().split('\n')
        prizes = re.findall(r'\d+', RaceData02[11])
        
        item = Race()
        item['race_id'] = re.search(r'race_id=(\d+)', response.url).group(1)
        item['race_date'] = response.css('dd.Active').xpath('string()').get()
        item['race_cource'] = RaceData02[2]
        item['round'] = response.css('span.RaceNum')[0].xpath('string()').get()
        item['race_name'] = response.css('div.RaceName').xpath('string()').get().strip()
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
            item['grade'] = re.search(r'class=.*\s(\w+)', response.css('div.RaceName > span.Icon_GradeType').get()).group(1)
        except TypeError:
            # grade競争以外はエラーとなるので、こちらを使用
            item['grade'] = ''

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
            item['cource_type'] = re.search(r'\s(\D+)', RaceData01).group(1)

        return item