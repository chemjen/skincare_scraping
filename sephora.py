from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random
import re
import os
import csv
import math

opts = Options()
opts.add_argument("user-agent=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']")
opts.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=opts)

product_urls = open('sephora_product_urls.txt', 'r').readlines()

########################################################################
if os.path.isfile(f'index.txt') and os.path.isfile(f'products.csv'):
	index = int(open('index.txt').read())
	index += 1
	if index >= len(product_urls) - 1:
		print(index)
		driver.close()
		raise SystemExit
	else: 
		csv_file =  open(f'products.csv', 'a', encoding='utf-8', newline='')
#		write = csv.writer(csv_file)
		writer = csv.DictWriter(csv_file, fieldnames = ['name', 'brand', 'family', 'genus', 'species',
			'price', 'size', 'weight', 'volume', 'num_loves', 'num_reviews', 'ave_rating', 
			'details', 'ingredients'])
		product_urls = product_urls[index:]
else:
	index = 0
	csv_file =  open(f'products.csv', 'w', encoding='utf-8', newline='')
#	writer = csv.writer(csv_file)
	writer = csv.DictWriter(csv_file, fieldnames = ['name', 'brand', 'family', 'genus', 'species',
			 'price', 'size', 'weight', 'volume', 'num_loves', 'num_reviews', 'ave_rating',
				'details', 'ingredients'])
	column_dict = {'name':'name', 'brand':'brand',  'family':'family', 'genus':'genus', 'species':'species',
					'price':'price', 'size':'size', 'weight':'weight', 'volume':'volume', 'num_loves':'num_loves',
					'num_reviews':'num_reviews', 'ave_rating':'ave_rating',
					'details':'details', 'ingredients':'ingredients'}
	writer.writerow(column_dict)	    

i = 0
unwanted_products = ['Mini Size', 'Value & Gift Sets', 'Facial Rollers', 'Brushes & Applicators', 
	'False Eyelashes', 'Rollerballs & Travel Size', 'Candles & Home Scents', 'Beauty Supplements',
	'High Tech Tools', 'Lip Sets', 'Face Sets', 'Eye Sets', 'Makeup Bags & Travel Accessories',
	'Tweezers & Eyebrow Tools', 'Blotting Papers', 'Hair Tools']
continue_shopping_xpath = '//div[@id="modalDialog"]//button[@aria-label="Continue shopping"]'

try:
	for i, url in enumerate(product_urls):
		product_dict = {}
		driver.get(url)
		time.sleep(5)
		driver.execute_script("setInterval(()=>document.querySelectorAll(\".modalDialog\").forEach(x=>x.remove()), 400)")
		time.sleep(2)
		product_type = driver.find_elements_by_xpath('//nav[@aria-label="Breadcrumbs"]//a')
		product_type = [val.text for val in product_type]
		if len(product_type) < 3:
			continue
		if (product_type[1] in unwanted_products) or (product_type[2] in unwanted_products):
			continue
		product = driver.find_elements_by_xpath('//h1[@data-comp="DisplayName Box "]//span')
		if len(product) == 0:
			product = driver.find_elements_by_xpath('//h1[@data-comp="DisplayName Flex Box"]//span')
		if len(product) == 0:
			print(url, 'did not work')
			continue

		product_dict['family'] = product_type[0]
		product_dict['genus'] = product_type[1]
		product_dict['species'] = product_type[2]
		product_dict['name'] = product[1].text
		product_dict['brand'] = product[0].text

		try:
			product_dict['price'] = driver.find_element_by_xpath('//div[@data-comp="Price Box "]').text 
		except:
			product_dict['price'] = driver.find_element_by_xpath('//div[@data-comp="Price Box "]/span[1]').text

	
		size = driver.find_element_by_xpath('//div[@data-comp="SizeAndItemNumber Box "]').text
		if re.findall('^ITEM', size):
			try:
				size = driver.find_element_by_xpath('//span[@data-comp="ProductVariation Text Box "]').text
				print(size)
			except:
				size = ''
	
		weight = re.findall("\d+\.?\d* ?oz", size)
		if weight:
			product_dict['weight'] = float(re.findall("\d+\.?\d*", weight[0])[0])
		weight = re.findall("\d+\.?\d* ?fl oz", size)
		if weight:
			product_dict['weight'] = float(re.findall("\d+\.?\d*", weight[0])[0])
		volume = re.findall("\d+ ?mL", size)
		if volume:	
			product_dict['volume'] = float(re.findall("\d+", volume[0])[0])
		product_dict['num_loves'] = driver.find_element_by_xpath('//span[@data-at="product_love_count"]').text
		product_dict['num_reviews'] = driver.find_element_by_xpath('//span[@data-at="number_of_reviews"]').text.split()[0]
	
		product_tabs_section = driver.find_elements_by_xpath('//div[@data-at="product_tabs_section"]')
		buttons = driver.find_elements_by_xpath('//div[@data-at="product_tabs_section"]/div[@aria-label="Product Information"]/button')
		driver.execute_script("window.scrollBy(0, 570)", product_tabs_section)
		time.sleep(5)

		print('going to product tab section')
	
		j = 0
		Details, Ingredients = '',''
		for button in buttons[:-1]:
			if j != 0:
				print('clicking tab')
				button.click()
				time.sleep(10)
			label = button.find_element_by_xpath('./span').text
			if label in ["Details", "Ingredients"]:
				text = [driver.find_element_by_xpath('//div[@id="tabpanel%d"]/div' %j).text]
				exec(f'{label} = {text}')
			if (Details != '') and (Ingredients != ''):
				break
			j += 1

		product_dict['details'] = Details
		product_dict['ingredients'] = Ingredients
		
		if product_dict['num_reviews'] != '0':
			review_section = driver.find_elements_by_xpath('//*[@id="ratings-reviews"]')
			driver.execute_script("window.scrollBy(0, 300)", review_section)
			time.sleep(10)
			ave_rating = driver.find_element_by_xpath('//*[@id="ratings-reviews"]//div[@class="css-1r36mik "]').text
			ave_rating = float(ave_rating.split('/')[0])
			print(ave_rating)
			product_dict['ave_rating'] = ave_rating

		writer.writerow(product_dict)
except Exception as e:
	print(url)
	print(e)
	open('tricky_pages.txt', 'a').write(url+'\n')
	open('index.txt', 'w').write('%d' %(i+index))
	csv_file.close()
	driver.close()
	time.sleep(10)
	quit()

driver.close()
quit()


