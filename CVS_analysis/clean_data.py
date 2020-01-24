import numpy as np
import pandas as pd

df = pd.read_csv('cvs_products.csv')

## I accidentally included a weight column in my scrape, but did not use it
df  = df.drop('weight', axis=1)

## the ounces column has some nans, so I fill in the rest by converting from 
## the pounds column
df['ounces_from_lbs'] = df['ounces']
oz_to_lbs = 16 #16 oz/lb
df['ounces_from_lbs'] = df['ounces_from_lbs'].fillna(df['pounds']*oz_to_lbs)

# I also did the reverse
df['lbs_from_oz'] = df['pounds']
df['lbs_from_oz'] = df['lbs_from_oz'].fillna(df['ounces']/oz_to_lbs)

## all the 'price' values are strings starting with '$', so I remove that and 
## convert to float
df['price'] = df['price'].apply(lambda x: float(x[1:]))

## create a 'price_per_oz' column
df['price_per_oz'] = df['price']/df['ounces_from_lbs']

## remove all gift and travel sets
df = df.loc[df['name'].apply(lambda x: 'gift set' not in x.lower())]
df = df.loc[df['name'].apply(lambda x: 'travel' not in x.lower())]

df = df.loc[~df['family'].isin(['health-medicine', 'vitamins'])] #, 'shop', 'household-grocery', 'personal-care'])]

#df = df.loc[(df['family'] != 'household-grocery') | (df['genus'] == 'as-seen-on-tv')]

#df = df.loc[(df['family'] != 'shop') | (df['genus'] == 'skin')]

#print(df.loc[df['family']=='shop'])
#print(df.loc[df['family']=='household-grocery'])

df.to_csv('cvs_products_cleaned.csv', index_label=False)

