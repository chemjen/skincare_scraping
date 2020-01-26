from check_sephora_urls.items import CheckSephoraUrlsItem
from scrapy import Spider, Request

class SephoraSpider(Spider):
	name = "sephora_spider"
	allowed_domains = ["https://www.sephora.com/"]
	start_urls = open('sephora_product_urls.txt', 'r').readlines()
	
	def parse(self, response):
		unwanted_products = ['Mini Size', 'Value & Gift Sets', 'Facial Rollers', 'Brushes & Applicators', 
			'False Eyelashes', 'Rollerballs & Travel Size', 'Candles & Home Scents', 'Beauty Supplements',
			'High Tech Tools', 'Lip Sets', 'Face Sets', 'Eye Sets', 'Makeup Bags & Travel Accessories',
			'Tweezers & Eyebrow Tools', 'Blotting Papers', 'Hair Tools']
		
		product_type = response.xpath('//nav[@aria-label="Breadcrumbs"]//a/text()').extract()
		print(product_type)
		if len(product_type) < 3:
			ischemical = ''
		elif (product_type[1] in unwanted_products) or (product_type[2] in unwanted_products):
			ischemical = 0
		else:			
			ischemical = 1
			
		product = response.xpath('//h1[@data-comp="DisplayName Box "]//span/text()').extract()
		if len(product) == 0:
			product = response.xpath('//h1[@data-comp="DisplayName Flex Box"]//span/text()').extract()

		item = CheckSephoraUrlsItem()
		item['ischemical'] = ischemical
		item['url'] = response.url
		item['product'] = product[1]
		item['brand'] = product[0]
		yield item


