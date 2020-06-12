# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class NetkeibaScrapingPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveToRaceResultByMySQLPipeline:

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

        self .conn.commit()

    def close_spider(self, spider):

        """ Spider の終了で MySQLサーバへの接続を切断する """

        self.conn.close()

    def process_item(self, item, spider):

        """ race_result に item を格納する """

        self.c.execute('INSERT IGNORE INTO `race_result` \
                        (`id`,`name`,`date`,`condition`,`entire_rap`,`ave_1F`,`first_half_ave_3F`,`last_half_ave_3F`,`RPCI`) \
                        VALUES (%(id)s, %(name)s, %(date)s, %(condition)s, %(entire_rap)s, %(ave_1F)s, %(first_half_ave_3F)s, %(last_half_ave_3F)s, %(RPCI)s)', dict(item))
        self.conn.commit()

        return item