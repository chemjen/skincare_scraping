import pandas as pd


urls = pd.read_csv('check_urls_with_scrapy/sephora_product_urls.csv')


urls = urls.loc[urls['ischemical'] =='1']

urls = urls['url'].values.flatten()

with open('sephora_chemical_urls.txt') as f:
	for url in urls:
		f.write(url+'\n')



