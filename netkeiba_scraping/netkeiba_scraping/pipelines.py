# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from netkeiba_scraping.items import RaceResult, HoseRaceResult, Hose, Race, RaceHose

class NetkeibaScrapingPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveToMySQLPipeline:

    """ item を MySQLに保存するPipeline """

    def open_spider(self, spider):

        """ MySQL に接続。
            テーブルがない時は作成する。 """

        settings = spider.settings

        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'netkeiba'),
            'user': settings.get('MYSQL_USER', ''),
            'passwd': settings.get('MYSQL_PASSWORD', ''),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }

        self.conn = MySQLdb.connect(**params)        
        self.c = self.conn.cursor()

        # テーブルが存在しなければ作成する
        # レース結果テーブル
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `race_result` (\
                `id` VARCHAR(12) NOT NULL, \
                `name` VARCHAR(200) NOT NULL, \
                `cource_id` VARCHAR(3) NOT NULL, \
                `cource_length` VARCHAR(5) NOT NULL, \
                `date` VARCHAR(11) NOT NULL, \
                `cource_type` VARCHAR(5) NOT NULL, \
                `cource_condition` VARCHAR(10) NOT NULL, \
                `entire_rap` VARCHAR(200) NOT NULL, \
                `ave_1F` DOUBLE(4,2) NOT NULL, \
                `first_half_ave_3F` DOUBLE(4,2) NOT NULL, \
                `last_half_ave_3F` DOUBLE(4,2) NOT NULL, \
                `RPCI` DOUBLE(4,2),
                `prize` VARCHAR(20), 
                `hose_all_number` VARCHAR(2),
                PRIMARY KEY(`id`)
                )
        """)

        # 各馬成績テーブル
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `hose_race_result` ( \
                `hose_id` VARCHAR(10) NOT NULL, \
                `race_id` VARCHAR(12) NOT NULL, \
                `gate_num` VARCHAR(2) NOT NULL, \
                `hose_num` VARCHAR(2) NOT NULL, \
                `odds` VARCHAR(6) NOT NULL, \
                `popularity` VARCHAR(2) NOT NULL, \
                `rank` VARCHAR(2) NOT NULL, \
                `jockey` VARCHAR(10) NOT NULL, \
                `burden_weight` VARCHAR(4) NOT NULL, \
                `time` VARCHAR(8) NOT NULL, \
                `time_diff` VARCHAR(5) NOT NULL, \
                `passing_order` VARCHAR(10) NOT NULL, \
                `last_3f` VARCHAR(5) NOT NULL, \
                `hose_weight` VARCHAR(4) NOT NULL, \
                `hose_weight_diff` VARCHAR(4) NOT NULL, \
                `get_prize` VARCHAR(20) NOT NULL, \
                PRIMARY KEY(`hose_id`, `race_id` )
            )
        """)

        # 競走馬基本情報テーブル
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `hose` ( \
                `hose_id` VARCHAR(10) NOT NULL, \
                `name` VARCHAR(20) NOT NULL, \
                PRIMARY KEY(`hose_id`)
            )
        """)

        # 出馬表テーブル
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `race` ( \
                `race_id` VARCHAR(12) NOT NULL, \
                `race_date` VARCHAR(10) NOT NULL, \
                `race_cource` VARCHAR(10) NOT NULL, \
                `round` VARCHAR(4) NOT NULL, \
                `race_name` VARCHAR(50) NOT NULL, \
                `grade` VARCHAR(20) NOT NULL, \
                `start_time` VARCHAR(6) NOT NULL, \
                `cource_type` VARCHAR(3) NOT NULL, \
                `distance` VARCHAR(5) NOT NULL, \
                `turn` VARCHAR(2) NOT NULL, \
                `side` VARCHAR(5) NOT NULL, \
                `days` VARCHAR(6) NOT NULL, \
                `regulation1` VARCHAR(20) NOT NULL, \
                `regulation2` VARCHAR(20) NOT NULL, \
                `regulation3` VARCHAR(20) NOT NULL, \
                `regulation4` VARCHAR(20) NOT NULL, \
                `prize1` VARCHAR(8) NOT NULL, \
                `prize2` VARCHAR(8) NOT NULL, \
                `prize3` VARCHAR(8) NOT NULL, \
                `prize4` VARCHAR(8) NOT NULL, \
                `prize5` VARCHAR(8) NOT NULL, \
                PRIMARY KEY(`race_id`)
            )
        """)

        # 出馬表-競走馬テーブルのCREATE文
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `race_hose` ( \
                `race_id` VARCHAR(12) NOT NULL, \
                `hose_id` VARCHAR(10) NOT NULL, \
                `gate_num` INTEGER, \
                `hose_num` INTEGER, \
                PRIMARY KEY(`race_id`, `hose_id`)
            )
        """)
    
        self .conn.commit()

    def close_spider(self, spider):

        """ Spider の終了で MySQLサーバへの接続を切断する """

        self.conn.close()

    def process_item(self, item, spider):

        """ DB に item を格納する """

        # race_result tableへの保存
        if isinstance(item, RaceResult):
            self.c.execute('INSERT IGNORE INTO `race_result` \
                            (`id`,`name`, `cource_id`, `cource_length`,`date`, `cource_type`, `cource_condition`, `entire_rap`,`ave_1F`,`first_half_ave_3F`,`last_half_ave_3F`,`RPCI`, `prize`, `hose_all_number`) \
                            VALUES (%(id)s, %(name)s, %(cource_id)s, %(cource_length)s, %(date)s, %(cource_type)s, %(cource_condition)s, %(entire_rap)s, %(ave_1F)s, %(first_half_ave_3F)s, %(last_half_ave_3F)s, %(RPCI)s, %(prize)s, %(hose_all_number)s)', dict(item))

            # 追加カラム、hose_all_numberの追加用
            # self.c.execute('UPDATE `race_result` SET `hose_all_number`=%(hose_all_number)s WHERE `id`=%(id)s', dict(item))

        # hose_race_result tableへの保存       
        if isinstance(item, HoseRaceResult):
            self.c.execute('INSERT IGNORE INTO `hose_race_result` \
                            (`hose_id`,`race_id`,`gate_num`,`hose_num`,`odds`,`popularity`,`rank`,`jockey`,`burden_weight`,`time`,`time_diff`,`passing_order`,`last_3f`,`hose_weight`,`hose_weight_diff`,`get_prize`) \
                            VALUES (%(hose_id)s,%(race_id)s,%(gate_num)s,%(hose_num)s,%(odds)s,%(popularity)s,%(rank)s,%(jockey)s,%(burden_weight)s,%(time)s,%(time_diff)s,%(passing_order)s,%(last_3f)s,%(hose_weight)s,%(hose_weight_diff)s,%(get_prize)s)', dict(item))

        # hose table への保存
        if isinstance(item, Hose):
            self.c.execute('INSERT IGNORE INTO `hose` \
                            (`hose_id`, `name`) \
                            VALUES (%(hose_id)s, %(name)s)', dict(item))

        # race table への保存
        if isinstance(item, Race):
            self.c.execute('INSERT IGNORE INTO `race` \
                            (`race_id`, `race_date`, `race_cource`, `round`, `race_name`, `grade`, `start_time`, `cource_type`, `distance`, `turn`, `side`, `days`,`regulation1`, `regulation2` ,`regulation3`, `regulation4`, `prize1`, `prize2`, `prize3`, `prize4`, `prize5`) \
                            VALUES (%(race_id)s, %(race_date)s, %(race_cource)s, %(round)s, %(race_name)s, %(grade)s, %(start_time)s, %(cource_type)s, %(distance)s, %(turn)s, %(side)s, %(days)s,%(regulation1)s, %(regulation2)s ,%(regulation3)s, %(regulation4)s, %(prize1)s, %(prize2)s, %(prize3)s, %(prize4)s, %(prize5)s)', dict(item))
                             
        # race_hose table への保存
        if isinstance(item, RaceHose):
            self.c.execute('INSERT IGNORE INTO `race_hose` \
                            (`race_id`, `hose_id`, `gate_num`, `hose_num`) \
                            VALUES (%(race_id)s, %(hose_id)s, %(gate_num)s, %(hose_num)s)', dict(item))

        self.conn.commit()

        return item