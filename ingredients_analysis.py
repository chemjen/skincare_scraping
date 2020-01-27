import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (5,5)
df = pd.read_csv('sephora_clean.csv')
bad_substances = open('banned_substances.txt', 'r').readlines()
bad_substances = list(set(bad_substances))
other_bad_ingredients = open('common_ingredients.txt', 'r').readlines()
common_substances = [x.strip() for x in other_bad_ingredients]
common_substances.append('fragrance')
cis = open('CIs.txt', 'r').readlines()
CIs = [x.strip() for x in cis]

df = df.loc[~df['name'].str.contains('mini')]
df = df.loc[~df['name'].str.contains('travel')]
df = df.loc[~(df['family'].str.contains('accessor')) |
           (df['genus'].str.contains('accessor')) |
           (df['species'].str.contains('accessor'))]

df_ingredients = df[['name','brand','ingredients']].dropna()
ingredients_list = df_ingredients['ingredients'].values.flatten()
ingredients_list = [x.split('clean at sephora products are formulated without:')[0] for x in ingredients_list]
false_positives = ['2', 'ethyl', 'tar','alpha','ammonium', 'bis', 'diethyl', 'urethane']

bad_ingredients_list = [x.strip() for x in bad_substances if x.strip() not in false_positives]
bad_ingredients_list.extend(['polyurethane-18', 'polyurethane-19'])#

safe_ingredients = ['chromium oxide greens', 'phenoxyethanol', 'cocam', 'hydroxyethyl acetate',
                   'polyvinyl acetate', 'starch', 'chromium hydroxide green', '1,2-hexanediol,', 'hydroxyethyl acrylate']
safe_ingredients = []
present_CIs = []
bad_ingredients_fullstring = []
for list_ in ingredients_list:
    lines = list_.split('\\n')
    lines = [line for line in lines if (len(line)>1) and line[0] != '-']
    list_ = ' '.join(lines)
    for word in safe_ingredients:
        list_ = list_.replace(word,'')
    bad_ingredients_fullstring.append([x for x in common_substances if x in list_])
    present_CIs.append([x for x in CIs if x in list_])

bad_ingredients_words = []
for list_ in ingredients_list:
#    bad_ingredients1 = []
#    bad_ingredients2 = []
    bad_ingredients = []
    lines = [x for x in list_.split('\\n') if len(x) > 1]
    for line in lines:
        ingdts = line.split(', ')
        words = []
        for ingdt in ingdts:
            words.extend(ingdt.split('/'))
        words = [word.strip() for word in words]
        for word in words:
            if (word in bad_ingredients_list):
                bad_ingredients.append(word)
#    bad_ingredients_words1.append(bad_ingredients1)
#    bad_ingredients_words2.append(bad_ingredients2)
    bad_ingredients_words.append(bad_ingredients)

special_ingredients = []
for list_ in ingredients_list:
    list_dict = {}
    lines = list_.split('\\n')
    special_lines = [line for line in lines if (len(line) > 0) and (line[0] == '-')]
    for line in special_lines:
        if len(line.split(':')) > 1:
            list_dict[line.split(':')[0][1:]] = line.split(':')[1]
        else:
            list_dict[line.split(':')[0][1:]] = ''
    special_ingredients.append(list_dict)

df_ingredients['EU banned ingredients'] = bad_ingredients_words
df_ingredients['common bad ingredients'] = bad_ingredients_fullstring
df_ingredients['special ingredients'] = special_ingredients

from itertools import chain
from collections import Counter

def count_df(nested_list, column_name):
    chained_list = chain.from_iterable(nested_list)
    count_dict = Counter(chained_list)
    return pd.DataFrame(list(count_dict.items()), columns=['ingredient',column_name])
    
def full_count_df(df):
    special_df = count_df(df['special ingredients'].values.flatten(), column_name = 'special counts')
    common_df = count_df(df['common bad ingredients'].values.flatten(), column_name = 'common counts')
    EU_df = count_df(df['EU banned ingredients'].values.flatten(), column_name = 'EU counts')
    new_df = pd.merge(special_df, common_df, how='outer', on='ingredient')
    return pd.merge(new_df, EU_df, how='outer', on='ingredient')

total_count_df = full_count_df(df_ingredients)

df_ingredients = pd.merge(df, df_ingredients, on=['name','brand','ingredients'])

bath_body = df_ingredients.loc[df_ingredients['family']=='Bath & Body']
fragrance = df_ingredients.loc[df_ingredients['family']=='Fragrance']
hair = df_ingredients.loc[df_ingredients['family']=='Hair']
makeup = df_ingredients.loc[df_ingredients['family']=='Makeup']
men = df_ingredients.loc[df_ingredients['family']=='Men']
skincare = df_ingredients.loc[df_ingredients['family']=='Skincare']
not_fragrance = df_ingredients.loc[~(df_ingredients['family']=='Fragrance')]

bb_count_df = full_count_df(bath_body)
frag_count_df = full_count_df(fragrance)
hair_count_df = full_count_df(hair)
makeup_count_df = full_count_df(makeup)
men_count_df = full_count_df(men)
skincare_count_df = full_count_df(skincare)
notfrag_count_df = full_count_df(not_fragrance)
#total_count_df['family'] = 'all'
#bb_count_df['family'] = 'bath_body'
#frag_count_df['family'] = 'fragrance'
#hair_count_df['family'] = 'hair'
#makeup_count_df['family'] = 'makeup'
#men_count_df['family'] = 'men'
#skincare_count_df['family'] = 'skincare'


dfs = [total_count_df, notfrag_count_df, bb_count_df, frag_count_df, makeup_count_df, men_count_df, skincare_count_df]
title = ['all products', 'everything but fragrance', 'bath & beauty', 'fragrance', 'makeup', 'men', 'skincare']
total_num = [df_ingredients.shape[0], not_fragrance.shape[0], bath_body.shape[0], fragrance.shape[0], makeup.shape[0], men.shape[0], skincare.shape[0]]
print(total_num)
for i, df in enumerate(dfs):
	df['ingredient'] = df['ingredient'].apply(lambda x: x.replace('hydroxyisohexyl 3-cyclohexene carboxaldehyde', 'h3cc'))

	dfnew = df[['ingredient', 'special counts']].dropna().sort_values(by='special counts', ascending=False)[:10]
	dfnew.plot.bar(x='ingredient', y='special counts')
	for j, val in enumerate(dfnew['special counts'][:10]):
		plt.text(j-0.25, val*1.01, '%1.1f%%' %(val*100/total_num[i]))
	plt.title(title[i])
	plt.tight_layout()
	plt.show()
	
	dfnew = df.loc[~df['ingredient'].str.contains('ci ')]	
	dfnew = dfnew[['ingredient', 'EU counts']].dropna().sort_values(by='EU counts', ascending=False)[:10]
	dfnew.plot.bar(x='ingredient', y='EU counts')
	for j, val in enumerate(dfnew['EU counts'][:10]):
		plt.text(j-0.25, val*1.01, '%1.1f%%' %(val*100/total_num[i]))
	plt.title(title[i])
	plt.tight_layout()
	plt.show()

	dfnew = df.loc[~df['ingredient'].str.contains('ci ')]	
	dfnew = dfnew[['ingredient', 'common counts']].dropna().sort_values(by='common counts', ascending=False)[:10]
	dfnew.plot.bar(x='ingredient', y='common counts')
	for j, val in enumerate(dfnew['common counts'][:10]):
		plt.text(j-0.25, val*1.01, '%1.1f%%' %(val*100/total_num[i]))
	plt.title(title[i])
	plt.tight_layout()
	plt.show()
#	dfnew = df['ingredients','common bad ingredients'].count().sort_values(ascending=False)[:20]
#	dfnew.plot.bar(x='ingredients', y='common bad ingredients')
#	for j, val in dfnew['ingredients'][:20]:
#		plt.text(j-0.1, val*1.05, '1.2%f %%' %(val*100/df.shape[0]))
#	plt.tight_plot()
#	plt.show()

#	dfnew = df['ingredients','EU banned ingredients'].count().sort_values(ascending=False)[:20]
#	dfnew.plot.bar(x='ingredients', y='EU banned ingredients')
#	for j, val in dfnew['ingredients'][:20]:
#		plt.text(j-0.1, val*1.05, '1.2%f %%' %(val*100/df.shape[0]))
#	plt.tight_plot()
#	plt.show()
quit()
def percent(x):
    num_x = x.sum()
    num_group = x.size
    return num_x/num_group*100

for df in [makeup, bath_body, skincare, hair, men]:

	df['contains EU ingredients'] = df['EU banned ingredients'].apply(lambda x: 1 if (len(x) > 0) else 0)
	df['contains common ingredients'] = df['common bad ingredients'].apply(lambda x: 1 if (len(x) > 0) else 0)
	df['contains either'] = df['contains EU ingredients'] + df['contains common ingredients']
	df['contains either'] = df['contains either'].apply(lambda x: 1 if x >= 1 else 0)

	nrows = df.shape[0]

	df_brands = df.groupby('brand').filter(lambda x: x.shape[0] > 9)
	brands = df_brands['brand'].unique()

	percent_contaminated = np.zeros(len(brands))
	median_price = np.zeros(len(brands))
	for i, brand in enumerate(brands):
		median_price[i] += df_brands.loc[df_brands['brand'] == brand]['price_per_oz'].median()
		percent_contaminated[i] += df_brands.loc[df_brands['brand'] ==brand]['contains either'].sum()/ df_brands.loc[df_brands['brand'] ==brand].shape[0]

	brand_agg_df = pd.DataFrame(list(zip(brands, median_price, percent_contaminated)), 
	columns=['brand', 'median price', 'percent contaminated'])
	brand_agg_df = brand_agg_df.sort_values(by='percent contaminated', ascending=False)

	print(brand_agg_df.corr())

	x = np.arange(len(brands))  # the label locations
	width = 0.25  # the width of the bars

	fig, ax1 = plt.subplots()
	rects1 = ax1.bar(x - width/2, brand_agg_df['percent contaminated'], width, label='percent bad', color="dodgerblue")

	ax1.set_xlabel('brand')
	ax1.set_ylabel('percent', color="dodgerblue", fontsize=16)
	ax1.set_title('price vs quality of ingredients')
	ax1.set_xticks(x)
	ax1.set_xticklabels(brand_agg_df['brand'], rotation=90)
	ax1.legend()
	ax2 = ax1.twinx()
	rects2 = ax2.bar(x + width/2, brand_agg_df['median price'], width, label='median price', color="salmon")
	ax2.set_ylabel('price', color="salmon", fontsize=16)
	plt.tight_layout()
	plt.show()



from scipy import stats
print(stats.binom_test(x=2403, n=5247, p=0.400)/2)
print(stats.binom_test(x=110, n=5247, p=0.017)/2)










