"""
    最終的に取得したいitemをperseするためのModule
    1. 単体で使うことはできない。
    2. 各Spider はこのClassをimportすること
    3. 永続化するitem を yieldする関数はこちらに記載すること 
"""

import scrapy
import re
from urllib.parse import urljoin
from netkeiba_scraping.items import RaceResult, HoseRaceResult, Hose, Race, RaceHose
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
        item['cource_id'] = re.search(r'/race/(\d+)', response.url).group(1)[4:6]
        item['cource_length'] = re.search(r'\d+', mainrace_data_span_array[0]).group(0)

        # TODO 'YYYY-M-DD'に変換して保存
        item['date'] = small_txt_p_array[0].replace('年', '-').replace('月', '-').replace('日', '')
        item['cource_type'] = re.search(r'(\S+) :',mainrace_data_span_array[4]).group(1)
        item['cource_condition'] = re.search(r': (\S+)',mainrace_data_span_array[4]).group(1)

        try:
            race_rap = response.css('td.race_lap_cell').xpath('string()').getall()[0]
        except IndexError:
            print('レースのラップが提供されていません。Skipします。')
            return

        race_rap_float_array = [float(x) for x in race_rap.replace(' ', '').split('-')]
        race_pace = response.css('td.race_lap_cell').xpath('string()').getall()[1]
        race_pace_float_array = [float(x) for x in re.search(r'\(([\d,.,-]+)', race_pace).group(1).split('-')]

        item['entire_rap'] = race_rap.replace(' ', '')
        
        # 3Fで割り切れないレースの場合、配列の初めは0.5F(100m)の距離となっているので * 2 して補正する。
        if int(item['cource_length']) % 200 != 0:
            race_rap_float_array[0] = race_rap_float_array[0] * 2    

        item['ave_1F'] = average(race_rap_float_array) 
        item['first_half_ave_3F'] = race_rap_float_array[0] + race_rap_float_array[1] + race_rap_float_array[2]
        item['last_half_ave_3F'] = race_rap_float_array[-1] + race_rap_float_array[-2] + race_rap_float_array[-3]
        item['RPCI'] = 50 * item['first_half_ave_3F'] / item['last_half_ave_3F']

        item['prize'] = response.css('.race_table_01 > tr')[1].css('td.txt_r').xpath('string()').getall()[-1].replace(',', '')

        item['hose_all_number'] = len(response.css('table.race_table_01 > tr').getall()) - 1

        return item

    def parse_race_result_from_sokuhou(self, response):

        """ レース結果情報を取得 """

        item = RaceResult()

        raceData01_array = response.css('div.RaceData01').xpath('string()').get().replace('\n', '').replace('/', '').split(' ')

        item['id'] = re.search(r'race_id=(\d+)', response.url).group(1)
        item['name'] = response.css('div.RaceName').xpath('string()').get().strip()
        item['cource_id'] = re.search(r'race_id=(\d+)', response.url).group(1)[4:6]
        item['cource_length'] = re.search(r'\d+', raceData01_array[2]).group(0)

        year = re.search(r'race_id=(\d+)', response.url).group(1)[0:4]
        month_day = re.search(r'(\S+)\(', response.css('dl#RaceList_DateList > dd.Active').xpath('string()').get()).group(1)
        
        # TODO 'YYYY-M-DD'に変換して保存
        item['date'] = year + '年' + month_day

        if re.search(r'[芝ダ障]', raceData01_array[2]).group(0) == '芝':
            item['cource_type'] = '芝'
        elif re.search(r'[芝ダ障]', raceData01_array[2]).group(0) == 'ダ':
            item['cource_type'] = 'ダート'
        elif re.search(r'[芝ダ障]', raceData01_array[2]).group(0) == '障':
            item['cource_type'] = '障害'
        else:
            item['cource_type'] = re.search(r'[芝ダ障]', raceData01_array[2]).group(0)
        
        if re.search(r':(\S+)', raceData01_array[5]).group(1) == '稍':
            item['cource_condition'] = '稍重'
        elif re.search(r':(\S+)', raceData01_array[5]).group(1) == '不':
            item['cource_condition'] = '不良'
        else:
            item['cource_condition'] = re.search(r':(\S+)', raceData01_array[5]).group(1)

        race_rap_array = response.css('tr.HaronTime').getall()[1].replace('</td>', '').replace('\n</tr>', '').split('<td>')[1:]
        race_rap_float_array = [ float(x) for x in race_rap_array ]
        item['entire_rap'] = '-'.join(race_rap_array)

        # 3Fで割り切れないレースの場合、配列の初めは0.5F(100m)の距離となっているので * 2 して補正する。
        if int(item['cource_length']) % 200 != 0:
            race_rap_float_array[0] = race_rap_float_array[0] * 2    

        item['ave_1F'] = average(race_rap_float_array) 
        item['first_half_ave_3F'] = race_rap_float_array[0] + race_rap_float_array[1] + race_rap_float_array[2]
        item['last_half_ave_3F'] = race_rap_float_array[-1] + race_rap_float_array[-2] + race_rap_float_array[-3]
        item['RPCI'] = 50 * item['first_half_ave_3F'] / item['last_half_ave_3F']

        raceData02_array = response.css('div.RaceData02 > span').xpath('string()').getall()
        item['prize'] = re.search(r':(\d+)', raceData02_array[-1]).group(1).replace(',', '')
        item['hose_all_number'] = re.search(r'(\d+)', raceData02_array[-2]).group(1)

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
        
        item = Race()

        # 中央競馬の時の処理
        if re.search(r'https://([\w.]+/)', response.url).group(1) == 'race.netkeiba.com/':
            prizes = re.findall(r'\d+', RaceData02[11])
            item['race_cource'] = RaceData02[2]
            item['days'] = RaceData02[3]
            item['regulation1'] = RaceData02[4]
            item['regulation2'] = RaceData02[5]
            item['regulation3'] = RaceData02[7]
            item['regulation4'] = RaceData02[8]
            item['round'] = response.css('span.RaceNum')[0].xpath('string()').get()

        # 地方競馬の時の処理
        if re.search(r'https://([\w.]+/)', response.url).group(1) == 'nar.netkeiba.com/':
            prizes = re.findall(r'[\d.]+', RaceData02[8])
            item['race_cource'] = RaceData02[2]
            item['days'] = RaceData02[3]
            item['regulation1'] = RaceData02[4]
            item['regulation2'] = ''
            item['regulation3'] = ''
            item['regulation4'] = ''
            item['round'] = response.css('div.RaceList_Item01 > div > span').xpath('string()').get()

        item['race_id'] = re.search(r'race_id=(\d+)', response.url).group(1)
        item['race_date'] = response.css('dd.Active').xpath('string()').get().strip()
        item['race_name'] = response.css('div.RaceName').xpath('string()').get().strip()
        item['distance'] = re.search(r'(\d+)m', RaceData01).group(1)
        item['turn'] = re.search(r'\((\D+)\)', RaceData01).group(1).split(' ')[0]
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

    def parse_race_hose(self, race_id, response):

        """ 出馬表-競走馬データを取得する """

        item = RaceHose()

        item['race_id'] = race_id
        item['hose_id'] = re.search(r'horse/(\d+)', response.css('span.HorseName > a::attr("href")').get()).group(1)
        
        try:
            item['gate_num'] = int(response.css('td').xpath('string()').getall()[0])
            item['hose_num'] = int(response.css('td').xpath('string()').getall()[1])
        except ValueError:
            item['gate_num'] = ''
            item['hose_num'] = ''

        return item