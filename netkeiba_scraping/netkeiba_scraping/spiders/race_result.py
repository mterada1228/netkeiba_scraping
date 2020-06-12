import scrapy
from scrapy.spiders import Rule
from netkeiba_scraping.spiders.module.parse_module import ParseModuleSpider

class RaceResultSpider(scrapy.Spider):

    name = 'race_result'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['https://db.netkeiba.com/race/202005020911/', 'https://db.netkeiba.com/race/202008010111/']

    def parse(self, response):
       yield ParseModuleSpider.parse_race_result(self, response)