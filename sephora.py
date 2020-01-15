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

start_url = "https://sephora.com/brands-list"

driver.get(start_url)
brands = driver.find_elements_by_xpath('//div//ul/li/a')

brands = [a.get_attribute('href')+'/all' for a in brands]

#		waited = WebDriverWait(driver, 10)
#		reviews = waiter.until(EC.presence_of_all_elements_located((By.XPATH,
#									'//div[@class="row border_grayThree onlyTopBorder noSideMargin"]')))


########################################################################
def scrape_brandpage(url, num_products):
	if url:
		driver.implicitly_wait(10)
		driver.get(url)	
#	else:
#		driver.refresh()
#		driver.execute_script("return document.documentElement.outerHTML")


	if (num_products > 12) and (num_products <= 36):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.60)")
		time.sleep(7)
	if (num_products > 36) and (num_products <= 48):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5)")
		time.sleep(5)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8)")
		time.sleep(5)	
	if (num_products > 48):
		product_xpath = '//div[@class="css-12egk0t"]/a[@class="css-ix8km1"]'
		try:
			driver.find_elements_by_xpath(product_xpath)[-1].click()
			driver.find_elements_by_xpath(product_xpath)[-1].send_keys(Keys.PAGE_DOWN)
		except:
			ex_out = driver.find_element_by_xpath('//div[@id="modalDialog"]//button[@aria-label="Continue shopping"]')
			time.sleep(2)
			ex_out.click()
			driver.find_elements_by_xpath(product_xpath)[-1].click()
			driver.find_elements_by_xpath(product_xpath)[-1].send_keys(Keys.PAGE_DOWN)
		time.sleep(5)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(5)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])		
		time.sleep(5)
		driver.execute_script("arguments[0].scrollIntoView()", driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(5)
	products = driver.find_elements_by_xpath('//div[@class="css-12egk0t"]/a[@class="css-ix8km1"]')
	product_urls = [product.get_attribute('href') for product in products]
	return product_urls

total_product_urls = []
for brand in brands:
	print(brand)
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
		brand_urls = scrape_brandpage(brand, 60)
		num_pages = math.ceil(num_tot_products/60.)
		num_last_page = num_tot_products % 60
		page_urls = [brand[:-4]+f'?currentPage={page}' for page in range(2, num_pages+1)]
		for i, page in enumerate(page_urls):
			try:
				next_page_button = driver.find_element_by_xpath('//nav[@aria-label="Pagination"]//button[@aria-label="Next"]')
				next_page_button.click()
			except:
				ex_out = driver.find_element_by_xpath('//div[@id="modalDialog"]//button[@aria-label="Continue shopping"]')				
				time.sleep(2)
				ex_out.click()
				next_page_button.click()
			time.sleep(5)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.60)")
			driver.execute_script("return document.documentElement.outerHTML")

			if i == (num_pages - 2):
				page_urls = scrape_brandpage([], num_last_page)
				brand_urls.extend(page_urls)
			else:
				brand_urls.extend(scrape_brandpage([], 60))

	num_brand_urls = len(brand_urls)
	assert num_tot_products == len(brand_urls), f"num_tot_products = {num_tot_products} and num_brand_urls = {num_brand_urls} ahhhh!"
	total_product_urls.extend(brand_urls)

print(len(total_product_urls))
with open(f'sephora_product_urls.txt', 'w') as f:
	for url in total_product_urls:
		f.write(url+'\n')

quit()
########################################################################

#driver.get("https://www.sephora.com/product/intensive-vitalizing-eye-essence-P394619?icid2=products%20grid:p394619")

driver.get("https://www.sephora.com/product/pro-filt-r-hydrating-primer-P448703?icid2=fenty_step1_011119_productcarousel_ufe:p448703:product")

cats = driver.find_elements_by_xpath('//nav[@aria-label="Breadcrumbs"]//a')
family, genus, species = cats[0].text, cats[1].text, cats[2].text

upper_right_box = driver.find_element_by_xpath('//div[@class="css-ehuxu5 "]')
price = driver.find_element_by_xpath('//div[@data-comp="Price Box"]').text[1:]
print('price')
print(price)
print('='*70)
product = driver.find_elements_by_xpath('//h1[@data-comp="DisplayName Flex Box"]//span')
print(len(product))
product = [x.text for x in product]
brand, product = product[0], product[1]
print('brand, product')
print(brand, product)
item = driver.find_element_by_xpath('//div[@data-comp="SizeAndItemNumber Box"]').text.split()[1]
print('item')
print(item)

try:
    size = driver.find_element_by_xpath('//div[@data-comp="SizeAndItemNumber Box"]/span').text
except:
    size = driver.find_element_by_xpath('//span[@data-comp="ProductVariation Text Box"]').text
print('size')
print(size)

num_love = driver.find_element_by_xpath('//div[@data-comp="ProductLovesCount Flex Box"]/span/span').text
print('num_love')
print(num_love)

num_reviews = driver.find_element_by_xpath('//a[@data-comp="RatingsSummary Flex Box"]/span').text.split()[0]
print('num_reviews')
print(num_reviews)

product_tabs_section = driver.find_element_by_xpath('//div[@data-at="product_tabs_section"]')

buttons = driver.find_elements_by_xpath('//div[@data-at="product_tabs_section"]/div[@aria-label="Product Information"]/button')
print(len(buttons))
#driver.execute_script("arguments[0].scrollIntoView", product_tabs_section)
driver.execute_script("window.scrollBy(0, 500)", product_tabs_section)
#time.sleep(5)
#driver.execute_script("document.getElementById('modalDialog').remove()")
wait_modal = WebDriverWait(driver, 10)
modal = wait_modal.until(EC.presence_of_all_elements_located((By.XPATH,
									'//div[@id="modalDialog"]')))
time.sleep(1)
modal[1].find_element_by_xpath('./button[@aria-label="Continue shopping"]').click()

i = 0
height = [450, 550, 450]

Details, Ingredients = [], []
for button in buttons[:-1]:
	if i != 0:
		button.click()
	label = button.find_element_by_xpath('./span').text
	if label in ["Details", "Ingredients"]:
#		print(label)
		text = [driver.find_element_by_xpath('//div[@id="tabpanel%d"]/div' %i).text]
#		print(text)
		print(len(text))
		exec(f'{label} = {text}')
	if (Details and Ingredients):
		break
	i += 1

print('Details, Ingredients')
print(Details, Ingredients)


ave_rating = driver.find_element_by_xpath('//*[@id="ratings-reviews"]/div[2]/div[2]/div[1]/div/div[1]/div[2]').text
print(ave_rating) 

would_recommend = driver.find_element_by_xpath('//*[@id="ratings-reviews"]/div[2]/div[2]/div[1]/div/div[2]/div').text

#driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2.)")
#details 
#ingredients

#rating

#most_helpful_review


#Rating 
#most_helpful_review





