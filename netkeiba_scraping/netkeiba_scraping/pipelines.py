# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from netkeiba_scraping.items import RaceResult
from netkeiba_scraping.items import HoseRaceResult

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
                `date` VARCHAR(11) NOT NULL, \
                `condition` VARCHAR(10) NOT NULL, \
                `entire_rap` VARCHAR(200) NOT NULL, \
                `ave_1F` DOUBLE(4,2) NOT NULL, \
                `first_half_ave_3F` DOUBLE(4,2) NOT NULL, \
                `last_half_ave_3F` DOUBLE(4,2) NOT NULL, \
                `RPCI` DOUBLE(4,2),
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

        self .conn.commit()

    def close_spider(self, spider):

        """ Spider の終了で MySQLサーバへの接続を切断する """

        self.conn.close()

    def process_item(self, item, spider):

        """ DB に item を格納する """

        # race_result tableへの保存
        if isinstance(item, RaceResult):
            self.c.execute('INSERT IGNORE INTO `race_result` \
                            (`id`,`name`,`date`,`condition`,`entire_rap`,`ave_1F`,`first_half_ave_3F`,`last_half_ave_3F`,`RPCI`) \
                            VALUES (%(id)s, %(name)s, %(date)s, %(condition)s, %(entire_rap)s, %(ave_1F)s, %(first_half_ave_3F)s, %(last_half_ave_3F)s, %(RPCI)s)', dict(item))

        # hose_race_result tableへの保存       
        if isinstance(item, HoseRaceResult):
            self.c.execute('INSERT IGNORE INTO `hose_race_result` \
                            (`hose_id`,`race_id`,`gate_num`,`hose_num`,`odds`,`popularity`,`rank`,`jockey`,`burden_weight`,`time`,`time_diff`,`passing_order`,`last_3f`,`hose_weight`,`hose_weight_diff`,`get_prize`) \
                            VALUES (%(hose_id)s,%(race_id)s,%(gate_num)s,%(hose_num)s,%(odds)s,%(popularity)s,%(rank)s,%(jockey)s,%(burden_weight)s,%(time)s,%(time_diff)s,%(passing_order)s,%(last_3f)s,%(hose_weight)s,%(hose_weight_diff)s,%(get_prize)s)', dict(item))

        self.conn.commit()

        return item