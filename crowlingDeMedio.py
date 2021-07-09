__author__ = 'ALEJANDRO'

import scrapy
from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from bs4 import BeautifulSoup

class KontraInfoItem(Item):
	titulo = Field()
	contenido = Field()

class KontraInfoCrawler(CrawlSpider):
	name = 'kontrainfocrawler'
	allowed_domains = ['kontrainfo.com']
	start_urls = ['https://kontrainfo.com']

	rules = (
		Rule(LinkExtractor(allow=r'/page/\d+'), follow=True),
		Rule(LinkExtractor(allow=r'/kontrainfo.com'), follow=True, callback='parse_items')
		)

	def parse_items(self, response):
		item = scrapy.loader.ItemLoader(KontraInfoItem(), response)
		item.add_xpath('titulo', '//h1/text()')

		soup = BeautifulSoup(response.body)
		article = soup.find('div',{'class':'entry-inner'})
		contenido = article.text
		item.add_value('contenido', contenido)

		yield item.load_item()



#min 18:44
# scrapy runspider crowlingDeMedio.py -o kontrainfo.csv -t csv --set CLOSESPIDER_ITEMCOUNT=20