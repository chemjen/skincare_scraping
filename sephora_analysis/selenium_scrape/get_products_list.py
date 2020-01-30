from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import csv
import math

### This is a script that goes to each brand page and gets the urls for each 
### product. It should be run second.
### The brand pages are set up such that in order to see the next page, 
### you have to click the "next page" at the bottom of the screen
### Each product shows up in it's own "lazy loading" div, meaning that in
### order for it to be "seen" the driver must scroll down to that element
### One challenge was dealing with the page "freezing", especially when the 
### number of products on the page was greater than about 40.  The 
### window needs to be reactivated by clicking on an element. However clicking
### on an element usually results in a  pop-up. Thus, the order of events in 
### the "scrape_brandpage_v1" function is to see if the elements are loading, 
### and if they are not, to try to click on the last visible element and then
### pass PAGE DOWN keys to it. If there is an exception, then there is a 
### popup, so the "continue shopping" button is clicked and then the PAGE
### DOWN keys are again passed to the element

### The pauses are really long because ironically "lazy loading" takes a long
### time and also this prevents the browser from crashing.

### Sometimes a pop-up would show up again after the second click, and then
### after clicking the "continue shopping" button, the page would 
### redirect to the url of the product element that was clicked. This usually 
### happens when the brand has two or more pages of products. Thus there is a 
### "scrape_brandpage_v2" function which after removing the first popup, first
###  passes PAGE DOWN before clicking then removes the pop-up again, then 
### clicks the element again. 

### There's also scraping_brandpage_v3, which did not need any clicking or 
### PAGE DOWNs after clicking the "continue shopping" button

### The change_page() function is for changing pages. This happens when 
### clicking the "Next button" at the bottom of the page. If the driver tries
### to find elements straight away, there is a "stale element" error, 
### however, refreshing the page results in the page returning to the first
### page of the brand. Thus the driver.execute_script("return document.\
### documentElement.outerHTML") command is run to get the elements on the page

### The maximum number of products per page is 60. Most brands have fewer than 
### 60 products, and thus just use scrape_brandpage_v1. The ones with between
### 60 and 120 products use num_pages_2() function, which scrapes the second 
### page with either v1 or v2. Only a few brands had more than 2 pages, with
### Clinique and Sephora being the only brands with more than 3 pages. These 
### use a combination of v1, v2, and v3.
##############################################################################

## setting up the webdriver with a user-agent and with options to 
## disable notifications - though it seems not to work well
opts = Options()
opts.add_argument("user-agent=['Mozilla/5.0 (Macintosh; Intel Mac OS X "
	"10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 "
	"Safari/537.36']")
opts.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=opts)

## open the brand page urls from the "get_brand_list.py" script
brands = open('sephora_brand_pages.txt', 'r').readlines()

## These are commonly used xpaths. The product_path is the path to the product
## urls the continue_shopping_xpath is the xpath to the "continue shopping" 
## button on the pop-up modal dialogs that come up
product_xpath = '//div[@class="css-12egk0t"]/a[@class="css-ix8km1"]'
continue_shopping_xpath = "//div[@id='modalDialog']//button[@aria-label="+\
	"'Continue shopping']"
## the driver.execute_script() method executes javascript code
## window_scroll is the command for scrolling, with document.body.scrollHeight
## being the length of the window
## usually it is used as
## driver.execute_script("window.scrollTo(0, document.body.scrollHeight*x)")
## where x is some fraction between 0 and 1 to determine how far down the page
## to scroll. Thus window_scroll(x) will scroll to that point on the page

def window_scroll(x):
	return f"window.scrollTo(0, document.body.scrollHeight*{x})"

############################################################################
## This is a function for scraping brand pages for product urls
def scrape_brandpage_v1(url, num_products):	
	if url:
		driver.implicitly_wait(10)
		driver.get(url)	
	if (num_products > 12) and (num_products <= 25):
		driver.execute_script(window_scroll(0.60))
		time.sleep(10)
	if (num_products > 25) and (num_products <= 36):
		driver.execute_script(window_scroll(0.6))
		time.sleep(10)
		driver.execute_script(window_scroll(0.4))
		time.sleep(10)	
		driver.execute_script(window_scroll(0.8))
		time.sleep(10)
	if (num_products > 36):
		nproducts_initial = len(driver.find_elements_by_xpath(product_xpath))
		if nproducts_initial <= 36:
			driver.execute_script("arguments[0].scrollIntoView()", \
				driver.find_elements_by_xpath(product_xpath)[-1])
			time.sleep(10)
			nproducts_final = len(driver.find_elements_by_xpath(product_xpath))
			if nproducts_initial == nproducts_final:
				try:
					driver.find_elements_by_xpath(product_xpath)[-1].click()
					time.sleep(5)
					driver.find_elements_by_xpath(product_xpath)[-1].\
						send_keys(Keys.PAGE_DOWN)
				except:
					time.sleep(10)
					ex_out = driver.\
						find_element_by_xpath(continue_shopping_xpath)
					time.sleep(5)
					ex_out.click()
					time.sleep(5)
					driver.find_elements_by_xpath(product_xpath)[-1].click()
					time.sleep(5)
					driver.find_elements_by_xpath(product_xpath)[-1].\
						send_keys(Keys.PAGE_DOWN)
		time.sleep(5)						
		driver.execute_script("arguments[0].scrollIntoView()", \
			driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
		driver.execute_script("arguments[0].scrollIntoView()", \
			driver.find_elements_by_xpath(product_xpath)[-1])		
		time.sleep(15)
		driver.execute_script(window_scroll(0.6))
		time.sleep(10)
		driver.execute_script("arguments[0].scrollIntoView()", \
			driver.find_elements_by_xpath(product_xpath)[-1])
		time.sleep(10)
	products = driver.find_elements_by_xpath(product_xpath)
	product_urls = [product.get_attribute('href') for product in products]
	return product_urls
	
def scrape_brandpage_v2():
	nproducts_initial = len(driver.find_elements_by_xpath(product_xpath))
	driver.execute_script("arguments[0].scrollIntoView()", driver.\
		find_elements_by_xpath(product_xpath)[-1])
	time.sleep(10)
	nproducts_final = len(driver.find_elements_by_xpath(product_xpath))
	if nproducts_initial == nproducts_final:
		driver.find_elements_by_xpath(product_xpath)[11].click()
		time.sleep(5)
		ex_out = driver.find_element_by_xpath(continue_shopping_xpath)	
		ex_out.click()
		time.sleep(3)
		driver.execute_script(window_scroll(0.8))
		time.sleep(15)
		nproducts  = len(driver.find_elements_by_xpath(product_xpath))
		if nproducts == nproducts_final:
			driver.find_elements_by_xpath(product_xpath)[5].\
				send_keys(Keys.PAGE_DOWN)
			time.sleep(15)
			nproducts  = len(driver.find_elements_by_xpath(product_xpath))
			driver.find_elements_by_xpath(product_xpath)[-1].click()
			time.sleep(5)
			ex_out = driver.find_element_by_xpath(continue_shopping_xpath)
			ex_out.click()
			time.sleep(0.5)
	driver.execute_script(window_scroll(0.2))
	time.sleep(2)
	driver.execute_script(window_scroll(0.5))
	time.sleep(15)
	driver.execute_script(window_scroll(0.8))
	time.sleep(5)
	driver.execute_script(window_scroll(0.615))
	time.sleep(15)
	products = driver.find_elements_by_xpath(product_xpath)
	product_urls = [product.get_attribute('href') for product in products]
	return product_urls

def scrape_brandpage_v3():
	nproducts_initial = len(driver.find_elements_by_xpath(product_xpath))
	driver.execute_script("arguments[0].scrollIntoView()", \
		driver.find_elements_by_xpath(product_xpath)[-1])
	time.sleep(10)
	nproducts_final = len(driver.find_elements_by_xpath(product_xpath))
	if nproducts_initial == nproducts_final:
		driver.find_elements_by_xpath(product_xpath)[11].click()
		time.sleep(5)
		ex_out = driver.find_element_by_xpath(continue_shopping_xpath)	
		ex_out.click()
		time.sleep(3)
		driver.execute_script(window_scroll(0.8))
		time.sleep(15)
		nproducts  = len(driver.find_elements_by_xpath(product_xpath))
	time.sleep(10)
	driver.execute_script(window_scroll(0.2))
	time.sleep(2)
	driver.execute_script(window_scroll(0.5))
	time.sleep(15)
	driver.execute_script(window_scroll(0.8))
	time.sleep(5)
	driver.execute_script(window_scroll(0.615))
	time.sleep(15)
	products = driver.find_elements_by_xpath(product_xpath)
	product_urls = [product.get_attribute('href') for product in products]
	return product_urls

def change_page():
	try:
		next_page_button = driver.find_element_by_xpath('//nav[@aria-label='+\
			'"Pagination"]//button[@aria-label="Next"]')
		next_page_button.click()
	except:
		ex_out = driver.find_element_by_xpath(continue_shopping_xpath)
		time.sleep(2)
		ex_out.click()
		time.sleep(2)
		next_page_button.click()
	time.sleep(2)
	driver.execute_script(window_scroll(0.60))
	time.sleep(4)
	driver.execute_script("return document.documentElement.outerHTML")
	time.sleep(15)
	
def num_pages_2(brand, num_tot_products, method):
	brand_urls = scrape_brandpage_v1(brand, 60)
	change_page()	
	if method == 1:
		brand_urls.extend(scrape_brandpage_v1([], num_tot_products-60))
	if method == 2:
		brand_urls.extend(scrape_brandpage_v2())
	return brand_urls

### these lines check to see if scrape has already started. Because of browser
### crashes or unexpected issues or accidentally closing the browser window, 
### the script will save what it has in sephora_product_urls.txt and then save 
### the index where it left off in index.txt, so that when rerun, the script 
### will simply start at that index and append to the existing urls
if os.path.isfile('index.txt') and os.path.isfile('sephora_product_urls.txt'):
	index = int(open('index.txt').read())
	f = open('sephora_product_urls.txt', 'a')
else:
	index = 0
	f = open('sephora_product_urls.txt', 'w')

### This is for running the scraper, different procedures are used depending  
### on how many product pages that brand has
try:
	for i, brand in enumerate(brands[index:]):
		driver.implicitly_wait(10)
		driver.get(brand)
		try:
			num_tot_products = int(driver.find_element_by_xpath('//span'+\
				'[@data-at="number_of_products"]').text.split()[0])
		except:
			num_tot_products = 0
			continue
		if num_tot_products <= 60:
			brand_urls = scrape_brandpage_v1(brand, num_tot_products) 
		elif num_tot_products <= 120:
			try:
				brand_urls = num_pages_2(brand, num_tot_products, 1)
			except:
				num_pages_2(brand, num_tot_products, 2)
		elif num_tot_products <= 180:
			brand_urls = num_pages_2(brand, num_tot_products, 2)
			change_page()
			brand_urls.extend(scrape_brandpage_v2())
		else:
			num_pages = math.ceil(num_tot_products/60) - 3
			num_last_page = num_tot_products % 60
			if num_last_page == 0:
				num_last_page = 60
			brand_urls = num_pages_2(brand, 120, 2)
			for _ in range(num_pages):
				change_page()
				brand_urls.extend(scrape_brandpage_v3())
			change_page()
			brand_urls.extend(scrape_brandpage_v2())

		for url in brand_urls:
			f.write(url+'\n')
except Exception as e:
	print(e)
	f.close()
	new_index = i+index
	open('index.txt', 'w').write('%d' %(i+index))

quit()
########################################################################


