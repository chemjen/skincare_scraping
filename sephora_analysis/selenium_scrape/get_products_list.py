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
	if (num_products > 25) and (num_products <= 36):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.6)")
		time.sleep(10)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.4)")
		time.sleep(10)	
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
		time.sleep(10)
	if (num_products > 36):
		nproducts_initial = len(driver.find_elements_by_xpath(product_xpath))
		if nproducts_initial <= 36:
			driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
			time.sleep(10)
			nproducts_final = len(driver.find_elements_by_xpath(product_xpath))
			if nproducts_initial == nproducts_final:
				try:
					print('clicking')
					driver.find_elements_by_xpath(product_xpath)[-1].click()
					print('clicked')
					time.sleep(5)
					print('page down')
					driver.find_elements_by_xpath(product_xpath)[-1].send_keys(Keys.PAGE_DOWN)
					print('paging down')
				except:
					time.sleep(10)
					ex_out = driver.find_element_by_xpath(continue_shopping_xpath)
					time.sleep(5)
					print('exing out')
					ex_out.click()
					time.sleep(5)
					print('clicking')
					driver.find_elements_by_xpath(product_xpath)[-1].click()
					time.sleep(5)
					print('paging down')
					driver.find_elements_by_xpath(product_xpath)[-1].send_keys(Keys.PAGE_DOWN)
		time.sleep(5)						
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])		
		time.sleep(15)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.6)")
#		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
#		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
	products = driver.find_elements_by_xpath(product_xpath)
	product_urls = [product.get_attribute('href') for product in products]
	print('no. product urls on this page =', len(product_urls))
	return product_urls
	
def scrape_multibrandpage():
	print('scraping')
	nproducts_initial = len(driver.find_elements_by_xpath(product_xpath))
	driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
	time.sleep(10)
	nproducts_final = len(driver.find_elements_by_xpath(product_xpath))
	if nproducts_initial == nproducts_final:
		print('trying to unfreeze page 1')
		driver.find_elements_by_xpath(product_xpath)[11].click()
		time.sleep(5)
		print('clicking out of dialog')
		ex_out = driver.find_element_by_xpath(continue_shopping_xpath)	
		ex_out.click()
		time.sleep(3)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
		time.sleep(15)
		nproducts  = len(driver.find_elements_by_xpath(product_xpath))
		print(nproducts)
		if nproducts == nproducts_final:
			print('here we go again')
			driver.find_elements_by_xpath(product_xpath)[5].send_keys(Keys.PAGE_DOWN)
			time.sleep(15)
			nproducts  = len(driver.find_elements_by_xpath(product_xpath))
			print(nproducts)
			driver.find_elements_by_xpath(product_xpath)[-1].click()
			time.sleep(5)
			ex_out = driver.find_element_by_xpath(continue_shopping_xpath)
			ex_out.click()
			time.sleep(0.5)
			print('clicked again')
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.2)")
	time.sleep(2)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5)")
	time.sleep(15)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.615)")
	time.sleep(15)
	products = driver.find_elements_by_xpath(product_xpath)
	product_urls = [product.get_attribute('href') for product in products]
	print('no. product urls on this page =', len(product_urls))
	return product_urls

def scrape_multibrandpage2():
	print('scraping')
	nproducts_initial = len(driver.find_elements_by_xpath(product_xpath))
	driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
	time.sleep(10)
	nproducts_final = len(driver.find_elements_by_xpath(product_xpath))
	if nproducts_initial == nproducts_final:
		print('trying to unfreeze page 1')
		driver.find_elements_by_xpath(product_xpath)[11].click()
		time.sleep(5)
		print('clicking out of dialog')
		ex_out = driver.find_element_by_xpath(continue_shopping_xpath)	
		ex_out.click()
		time.sleep(3)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
		time.sleep(15)
		nproducts  = len(driver.find_elements_by_xpath(product_xpath))
		print(nproducts)
	time.sleep(10)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.2)")
	time.sleep(2)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5)")
	time.sleep(15)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.615)")
	time.sleep(15)
	products = driver.find_elements_by_xpath(product_xpath)
	product_urls = [product.get_attribute('href') for product in products]
	print('no. product urls on this page =', len(product_urls))
	return product_urls










def change_page():
	print('changing page')
	try:
		next_page_button = driver.find_element_by_xpath('//nav[@aria-label="Pagination"]//button[@aria-label="Next"]')
		next_page_button.click()
	except:
		ex_out = driver.find_element_by_xpath(continue_shopping_xpath)
		time.sleep(2)
		ex_out.click()
		time.sleep(2)
		next_page_button.click()
	time.sleep(2)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.60)")
	time.sleep(4)
	driver.execute_script("return document.documentElement.outerHTML")
	time.sleep(15)
	

def num_pages_2(brand, num_tot_products, method):
	brand_urls = scrape_brandpage(brand, 60)
	change_page()	
	if method == 1:
		brand_urls.extend(scrape_brandpage([], num_tot_products-60))
	if method == 2:
		brand_urls.extend(scrape_multibrandpage())
	return brand_urls

if os.path.isfile('sephora_product_urls.txt'):
	f = open('sephora_product_urls.txt', 'a')
else:
	f = open('sephora_product_urls.txt', 'w')

largest_brands = open('largest_brands.txt', 'r').readlines()
largest_brands = [x for x in largest_brands if x != '']
index = 1

try:
	for i, brand in enumerate(largest_brands[index:]):
		print(i+ index, brand)
		driver.implicitly_wait(10)
		driver.get(brand)
		try:
			num_tot_products = int(driver.find_element_by_xpath('//span[@data-at="number_of_products"]').text.split()[0])
		except:
			num_tot_products = 0
			continue
		if num_tot_products <= 60:
			continue
			brand_urls = scrape_brandpage(brand, num_tot_products) 
		elif num_tot_products <= 120:
			continue
			try:
				brand_urls = num_pages_2(brand, num_tot_products, 1)
			except:
				num_pages_2(brand, num_tot_products, 2)
		elif num_tot_products <= 180:
			continue
			try:
				brand_urls = num_pages_2(brand, num_tot_products, 2)
				change_page()
				brand_urls.extend(scrape_multibrandpage())
			except:
				print(i, num_tot_products, brand, 'fail')
		else:
				num_pages = math.ceil(num_tot_products/60) - 3
				num_last_page = num_tot_products % 60
				if num_last_page == 0:
					num_last_page = 60
				brand_urls = num_pages_2(brand, 120, 2)
				for _ in range(num_pages):
					change_page()
					brand_urls.extend(scrape_multibrandpage2())
				#	brand_urls.extend(scrape_brandpage([],60))
				change_page()
				brand_urls.extend(scrape_multibrandpage())

		num_brand_urls = len(brand_urls)
#		assert num_tot_products == len(brand_urls), f"num_tot_products = {num_tot_products} and num_brand_urls = {num_brand_urls} ahhhh!"
#		total_product_urls.extend(brand_urls)
		for url in brand_urls:
			f.write(url+'\n')
except Exception as e:
	print(e)
	f.close()
	new_index = i+index
	open('index.txt', 'w').write('%d' %(i+index))

quit()
########################################################################


