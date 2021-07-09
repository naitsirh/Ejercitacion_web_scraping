__author__ = 'ALEJANDRO'

from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class AirbnbItem(Item):
	tipo = Field()
	capacidad = Field()

class AirbnbCrawler(CrawlSpider):
	name = "MiPrimerCrawler"
	start_urls = ["https://www.airbnb.com.ar/s/all?refinement_paths%5B%5D=%2Fhomes&query=Londres%2C+Reino+Unido"]
	allowed_domains = ['airbnb.com.ar']

	rules = (
		Rule(LinkExtractor(allow=r'offset=')),
		Rule(LinkExtractor(allow=r'/rooms'), callback='parse_items')
		)

	def parse_items(self, response):
		item = ItemLoader(AirbnbItem(), response)
		item.add_xpath('tipo', '/html/body/div[4]/div/div/div/div/div/div[1]/main/div/div/div[3]/div[1]/div/div[1]/div/div/div/div/div/div[1]/div[2]/span[3]/text()')
		item.add_xpath('capacidad', '/html/body/div[4]/div/div/div/div/div/div[1]/main/div/div/div[3]/div[1]/div/div[1]/div/div/div/div/div/div[1]/div[2]/span[1]/text()', MapCompose(lambda i: i(0)))
		yield item.load_item()



# scrapy runspider crowlingDeMedio.py -o kontrainfo.csv -t csv --set CLOSESPIDER_ITEMCOUNT=20