from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("user-agent=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']")
opts.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=opts)

start_url = "https://sephora.com/brands-list"

driver.get(start_url)
brands = driver.find_elements_by_xpath('//div//ul/li/a')

brands = [a.get_attribute('href')+'/all' for a in brands]

with open('sephora_brand_pages.txt', 'w') as f:
	for url in brands:
		f.write(url+'\n')

