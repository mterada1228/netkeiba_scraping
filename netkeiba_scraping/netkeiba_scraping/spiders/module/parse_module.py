"""
    最終的に取得したいitemをperseするためのModule
    1. 単体で使うことはできない。
    2. 各Spider はこのClassをimportすること
    3. 永続化するitem を yieldする関数はこちらに記載すること 
"""

import scrapy
import re
from urllib.parse import urljoin
from netkeiba_scraping.items import RaceResult
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