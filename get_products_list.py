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

brands = open('sephora_brand_pages.txt', 'r').readlines()
	
print(len(brands))
#		waited = WebDriverWait(driver, 10)
#		reviews = waiter.until(EC.presence_of_all_elements_located((By.XPATH,
#									'//div[@class="row border_grayThree onlyTopBorder noSideMargin"]')))

product_xpath = '//div[@class="css-12egk0t"]/a[@class="css-ix8km1"]'
continue_shopping_xpath = '//div[@id="modalDialog"]//button[@aria-label="Continue shopping"]'

########################################################################
def scrape_brandpage(url, num_products):
	if url:
		driver.implicitly_wait(10)
		driver.get(url)	

	if (num_products > 12) and (num_products <= 25):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.60)")
		time.sleep(10)
	if (num_products > 25) and (num_products <= 34):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.6)")
		time.sleep(10)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.4)")
		time.sleep(10)	
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
		time.sleep(10)
	if (num_products > 34):
		nproducts_initial = len(driver.find_elements_by_xpath(product_xpath))
		print(nproducts_initial)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
		nproducts_final = len(driver.find_elements_by_xpath(product_xpath))
		print(nproducts_final)
		if nproducts_initial == nproducts_final:
			try:
				print('trying to unfreeze page')
				driver.find_elements_by_xpath(product_xpath)[-1].click()
				time.sleep(5)
				print('paging down')
				driver.find_elements_by_xpath(product_xpath)[-1].send_keys(Keys.PAGE_DOWN)
			except:
				time.sleep(10)
				ex_out = driver.find_element_by_xpath(continue_shopping_xpath)
				time.sleep(5)
				print('clicking x out')
				ex_out.click()
#				print('clicking unloved button')
#				print(len(driver.find_elements_by_xpath('//div[@id="modalDialog"]//button')))
#				addto_loves = driver.find_elements_by_xpath('//div[@id="modalDialog"]//button')[2]
#				addto_loves.click()
#				time.sleep(3)
#				driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
#				time.sleep(2)
#				print('clicking x out')
#				button = driver.find_element_by_xpath(continue_shopping_xpath)
#				time.sleep(3)
#				button.click()
				time.sleep(5)
#				try:
#					print('trying to unfreeze again')
				driver.find_elements_by_xpath(product_xpath)[-1].click()
				time.sleep(5)
				driver.find_elements_by_xpath(product_xpath)[-1].send_keys(Keys.PAGE_DOWN)
#				time.sleep(10)
#				except:
#					print('clicking x out again')
#					ex_out = driver.find_element_by_xpath(continue_shopping_xpath)
#					time.sleep(0.5)
#					ex_out.click()				
#					time.sleep(3)
#					print('trying to unfreeze 3')
#					driver.find_elements_by_xpath(product_xpath)[-1].click()
#					time.sleep(3)
#					driver.find_elements_by_xpath(product_xpath)[-1].send_keys(Keys.PAGE_DOWN)
#					time.sleep(10)

		time.sleep(5)						
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])		
		time.sleep(15)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
	products = driver.find_elements_by_xpath(product_xpath)
	product_urls = [product.get_attribute('href') for product in products]
#	print('no. product urls on this page =', len(product_urls))
	return product_urls

total_product_urls = []

if os.path.isfile('sephora_product_urls.txt'):
	f = open('sephora_product_urls.txt', 'a')
else:
	f = open('sephora_product_urls.txt', 'w')
larger_brands = open('larger_brands.txt', 'r').readlines()
g = open('indices_of_larger_brands.txt', 'a')
index = int(open('index.txt', 'r').read())
if index == len(larger_brands)-1:
	quit()

#indices_of_larger_brands = open('indices_of_larger_brands.txt', 'r').readlines()
#indices_of_larger_brands = [int(i) for i in indices_of_larger_brands]
#print(indices_of_larger_brands)

#print(brands)
#larger_brands = []
#for i, brand in enumerate(brands):
#	if i in indices_of_larger_brands:
#		print(brands[i])
#		larger_brands.extend([brands[i]])
#print(larger_brands)

#with open('larger_brands.txt','w') as h:
#	for brand in larger_brands:
#		h.write(brand+'\n')
#print('rawr')
#quit()
larger_brands = [x.strip('\n') for x in larger_brands]
larger_brands = [x for x in larger_brands if x != '']
print(larger_brands)
print(len(larger_brands))
try:
	for i, brand in enumerate(larger_brands[index:]):
		print(i+ index, brand)
		driver.implicitly_wait(10)
		driver.get(brand)
		try:
			num_tot_products = int(driver.find_element_by_xpath('//span[@data-at="number_of_products"]').text.split()[0])
		except:
			num_tot_products = 0
			continue
		if num_tot_products <= 60:
			brand_urls = scrape_brandpage(brand, num_tot_products) 
		else:
			if num_tot_products > 120:
				g.write('%d\n' %(i+index))
				print(num_tot_products, 'not doing right now')
				continue
			print(num_tot_products)
			brand_urls = scrape_brandpage(brand, 60)
			num_pages = math.ceil(num_tot_products/60.)
			num_last_page = num_tot_products % 60
			page_urls = [brand[:-4]+f'?currentPage={page}' for page in range(2, num_pages+1)]
			for j, page in enumerate(page_urls):
				try:
					print('trying next page button')
					next_page_button = driver.find_element_by_xpath('//nav[@aria-label="Pagination"]//button[@aria-label="Next"]')
					next_page_button.click()
				except:
					print('dealing with modal dialog')
					ex_out = driver.find_element_by_xpath('//div[@id="modalDialog"]//button[@aria-label="Continue shopping"]')				
					time.sleep(2)
					ex_out.click()
					print('trying next page again')
					next_page_button.click()
				time.sleep(10)
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.60)")
				time.sleep(10)
				driver.execute_script("return document.documentElement.outerHTML")
				time.sleep(10)

				if j == (num_pages - 2):
					page_urls = scrape_brandpage([], num_last_page)
					brand_urls.extend(page_urls)
				else:
					brand_urls.extend(scrape_brandpage([], 60))

		num_brand_urls = len(brand_urls)
		assert num_tot_products == len(brand_urls), f"num_tot_products = {num_tot_products} and num_brand_urls = {num_brand_urls} ahhhh!"
#		total_product_urls.extend(brand_urls)
		for url in brand_urls:
			f.write(url+'\n')
except Exception as e:
	print(e)
	f.close()
	new_index = i+index
	open('index.txt', 'w').write('%d' %(i+index))
	g.close()
quit()
########################################################################


