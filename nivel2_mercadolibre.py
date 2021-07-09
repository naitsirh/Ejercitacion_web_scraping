from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader



class Articulo(Item):
	titulo = Field()
	precio = Field()
	descripcion = Field()

class MercadoLibreCrawler(CrawlSpider):
	name = 'mercadoLibre'
	custom_settings = {
		'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
		'CLOSESPIDER_PAGECOUNT': 20
	}

	download_delay = 5

	allowed_domains = ['listado.mercadolibre.com.ar', 'articulo.mercadolibre.com.ar']

	start_urls = ['https://listado.mercadolibre.com.ar/animales-mascotas/perros/']

	rules = (
		# La primera regla determina la paginación
		Rule(
			LinkExtractor(
				allow=r'/_Desde_'
				), follow=True
			),
		# La segunda regla determina cómo ir al detalle de los productos
		Rule(
			LinkExtractor(
				allow=r'/MLA-'
				), follow=True, callback='parse_items'
			)
		)


def limpiarTexto(self, texto):
	nuevoTexto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
	return nuevoTexto


def parse_items(self, response):
	item = ItemLoader(Articulo(), response)

	item.add_xpath('titulo', '//h1/text()', MapCompose(self.limpiarTexto))
	item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()', MapCompose(self.limpiarTexto))
	item.add_xpath('precio', '//span[@class="price-tag-fraction"]/text()')

	yield item.load_item()



#opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
#opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

#min 24:57