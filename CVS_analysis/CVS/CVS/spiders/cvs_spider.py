from CVS.items import CvsItem
from scrapy import Spider, Request
import re

## write a list of urls for the pages listing products
num_pages = 497
pages = ["https://www.cvs.com/shop/beauty?page="+ str(x) for x in range(2,num_pages+1)]

class cvs_spider(Spider):
	name = "cvs_spider"
	allowed_urls = ["https://www.cvs.com/"]
	start_urls = ['https://www.cvs.com/shop/beauty'] + pages
	
	def parse(self, response):
		## get the urls to the product pages
		product_urls = response.xpath('//div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n"]//a[contains(@href, "/shop/")]/@href').extract()
		## remove urls that are actually review pages or brand pages, and not product pages
		product_urls = [ url for url in product_urls if (url.find('reviews') == -1) and (url.find('/brand-shop/') == -1)]
		## write the full url
		product_urls = ["https://www.cvs.com" + url for url in product_urls]
		
		## send each url for parsing
		for url in product_urls:
			yield Request(url=url, callback=self.parse_product_page)

	def parse_product_page(self, response):
		## get the product name
		name = response.xpath('//*[@id="root"]//h1[@aria-level="1"]/text()').extract_first()
		
		## there are many elements with "$" in the text, but only one of the form "$XXX.XX"  
		price = response.xpath('//*[contains(text(), "$")]/text()').extract()
		price = list(filter(lambda x: len(x) <= 7 , price))[0]
		
		## find the element of the form "XX OZ .XX lbs. ITEM #XXXXXXX", if it exists, and assign it to weight
		try:
			weight = response.xpath('//div[@dir="auto"][@class="css-901oao r-1jn44m2 r-1enofrn"]/text()').extract_first()
		except:
			weight = ''
		
		## find the "XX OZ" part and assign it ounces, if it exists
		ounces = re.findall('(^\d+\.?\d*|^\.\d+) oz', weight.lower())
		if ounces:
			ounces = ounces[0]
		else:
			ounces = ''

		## find the ".XX lbs" part and assign it to pounds, if it exists
		pounds = re.findall('( \d+\.?\d*| \.\d+) lbs', weight.lower())
		if pounds:
			pounds = pounds[0]	
		else:
			pounds = ''

		## find the average rating and number of reviews, if it has been reviewsed 
		try:
			rating = response.xpath('//section[contains(@aria-label,"Rated")]/@aria-label').extract_first().split()[1]
			num_reviews= response.xpath('//*[@class="css-1dbjc4n r-obd0qt r-18u37iz"]/div[2]/text()').extract()[1]
		except:
			rating, num_reviews = '', ''

		## find the "see more from this brand link, which is of the form "https://cvs.com/brand-shop/brand-name/"
		brand = response.xpath('//a[@data-class="see-all-brand-link"]/@href').extract_first()
		brand = brand.split('/')[-1]

		## extract the links at the top of the page for the headings, the last link is of the form "https://cvs.com/shop/family/genus/species/"
		fgs = response.xpath('//div[@class="css-1dbjc4n r-1awozwy r-18u37iz r-3hmvjm r-1hvjb8t r-15zeulg"]/a[contains(@href, "/shop/")]/@href').extract()[-1]
		family = fgs.split('/')[-3]
		genus = fgs.split('/')[-2]
		species = fgs.split('/')[-1]

		## find the text with all the details
		detailpath = response.xpath('//div[@class="htmlView"][1]//text()').extract() 
		details = [x.strip() for x in detailpath if '}' not in x]
		newdetails = ' '.join(details)
		
		item = CvsItem()
		item['name'] = name
		item['brand'] = brand
		item['family'] = family
		item['genus'] = genus
		item['species'] = species
		item['url'] = response.url
		item['price'] = price
		item['ounces'] = ounces
		item['pounds'] = pounds
		item['details'] = newdetails
		item['num_reviews'] = num_reviews
		item['ave_rating'] = rating
		yield item


		
