"""
    最終的に取得したいitemをperseするためのModule
    1. 単体で使うことはできない。
    2. 各Spider はこのClassをimportすること
    3. 永続化するitem を yieldする関数はこちらに記載すること 
"""

import scrapy
import re
from urllib.parse import urljoin
from netkeiba_scraping.items import RaceResult, HoseRaceResult
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