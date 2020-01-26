import pandas as pd

df = pd.read_csv('all_sephora_products.csv')     
df = df.drop('size', axis=1)                       

df['price'] = df['price'].apply(lambda x: float(x.split()[0][1:]))     

oz_to_mL = 29.5735
df['oz_from_mL'] = df['weight']  
df['oz_from_mL'] = df['oz_from_mL'].fillna(df['volume']/oz_to_mL)  

df['num_reviews'] = df['num_reviews'].str.replace('K','000')

df['num_reviews'] = df['num_reviews'].astype(int)

df['price_per_oz'] = df['price']/df['oz_from_mL']

df['brand'] = df['brand'].str.lower()
df['name'] = df['name'].str.lower()

df['details'] = df['details'].str.lower()
df['ingredients'] = df['ingredients'].str.lower()
#df['ingredients'] = df['ingredients'].apply(lambda x: x.split('clean at sephora products are formulated without:')[0])

new_loves = []
num_loves = df['num_loves'].values.flatten()
for i, val in enumerate(num_loves):
	val = val.split('.')
	if len(val) == 2:
		new_loves.append(''.join(val).replace('K','00').replace('M','00000'))
	else:
		new_loves.append(val[0].replace('K','000').replace('M','000000'))
#	if 'M' and '.' in val:
#		print(val, val.replace('M','00000'))
#		new_loves.append(val.replace('.','').replace('M','00000'))
#	elif 'M' in val:
#		new_loves.append(val.replace('M','000000'))
#	elif '.' and 'K' in val:
#		new_loves.append(val.replace('.','').replace('K','00'))
#	elif 'K' in val:
#		print(val, val.replace('K','000'))
#		new_loves.append(val.replace('K','000'))
#	else:
#		new_loves.append(val)
df['num_loves'] = new_loves
df['num_loves'] = df['num_loves'].astype(int)
df.to_csv('sephora_clean.csv', index=False)                                                                           

