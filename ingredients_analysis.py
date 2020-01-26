import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,7)
df = pd.read_csv('sephora_clean.csv')
bad_substances1 = open('banned_substances.txt', 'r').readlines()
bad_substances2 = open('banned_substances2.txt', 'r').readlines()
bad_substances3 = open('banned_substances3.txt', 'r').readlines()
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

bad_ingredients_list1 = [x.strip() for x in bad_substances1 if x.strip() not in false_positives]
bad_ingredients_list1.extend(['polyurethane-18', 'polyurethane-19'])#
bad_ingredients_list2 = [x.strip() for x in bad_substances2 if x.strip() not in false_positives]
bad_ingredients_list2.extend(['polyurethane-18', 'polyurethane-19'])
bad_ingredients_list3 = [x.strip() for x in bad_substances3 if x.strip() not in false_positives]
bad_ingredients_list3.extend(['polyurethane-18', 'polyurethane-19'])

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
        ingdts = line.split(',')
        words = []
        for ingdt in ingdts:
            words.extend(ingdt.split('/'))
        words = [word.strip() for word in words]
        for word in words:
            if (word in bad_ingredients_list1) or (word in bad_ingredients_list2) \
               or (word in bad_ingredients_list3):
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

#plt.figure(figsize=(7,4))
#total_count_df.sort_values(by='special counts', ascending=False)[:20].plot.bar(x='ingredient',y='special counts')
#plt.tight_layout()
#plt.show()

#plt.figure(figsize=(7,4))
#total_count_df.sort_values(by='common counts', ascending=False)[:20].plot.bar(x='ingredient',y='common counts')
#plt.tight_layout()
#plt.show()

#plt.figure(figsize=(7,4))
#total_count_df.loc[~total_count_df['ingredient'].str.startswith('ci')].sort_values(by='EU counts', ascending=False)[:20].plot.bar(x='ingredient',y='EU counts')
#plt.tight_layout()
#plt.show()

df_ingredients = pd.merge(df, df_ingredients, on=['name','brand','ingredients'])

bath_body = df_ingredients.loc[df_ingredients['family']=='Bath & Body']
fragrance = df_ingredients.loc[df_ingredients['family']=='Fragrance']
hair = df_ingredients.loc[df_ingredients['family']=='Hair']
makeup = df_ingredients.loc[df_ingredients['family']=='Makeup']
men = df_ingredients.loc[df_ingredients['family']=='Men']
skincare = df_ingredients.loc[df_ingredients['family']=='Skincare']

bb_count_df = full_count_df(bath_body)
frag_count_df = full_count_df(fragrance)
hair_count_df = full_count_df(hair)
makeup_count_df = full_count_df(makeup)
men_count_df = full_count_df(men)
skincare_count_df = full_count_df(skincare)

total_count_df['family'] = 'all'
bb_count_df['family'] = 'bath_body'
frag_count_df['family'] = 'fragrance'
hair_count_df['family'] = 'hair'
makeup_count_df['family'] = 'makeup'
men_count_df['family'] = 'men'
skincare_count_df['family'] = 'skincare'

dfs = [total_count_df, bb_count_df, frag_count_df, makeup_count_df, men_count_df, skincare_count_df]
title = ['all products', 'bath & beauty', 'fragrance', 'makeup', 'men', 'skincare']
total_num = [df_ingredients.shape[0], bath_body.shape[0], fragrance.shape[0], makeup.shape[0], men.shape[0], skincare.shape[0]]
for i, df in enumerate(dfs):
#	dfnew = df[['ingredient', 'special counts']].dropna()
#	dfnew.sort_values(by='special counts', ascending=False)[:20].plot.bar(x='ingredient',y='special counts')
#	for j, count in enumerate(dfnew.sort_values(by='special counts', ascending=False)['special counts'][:20]):
#		plt.text(j-0.25, 1.01*count, '%2.1f%%' %(count/total_num[i]*100))
#	plt.title(title[i])
#	plt.tight_layout()
#	plt.show()
	
#	newdf = df.loc[~(df['ingredient'] == 'acrylate')]
#	newdf = df[['ingredient', 'common counts']].dropna()
#	newdf.sort_values(by='common counts', ascending=False)[:20].plot.bar(x='ingredient',y='common counts')
#	for j, count in enumerate(newdf.sort_values(by='common counts', ascending=False)['common counts'][:20]):
#		plt.text(j-0.25, 1.01*count, '%2.1f%%' %(count/total_num[i]*100))

#	plt.title(title[i])
#	plt.tight_layout()
#	plt.show()

	newdf = df.loc[~df['ingredient'].str.contains('ci ')]
	newdf = newdf[['ingredient', 'EU counts']].dropna()
	newdf.sort_values(by='EU counts', ascending=False)[:20].plot.bar(x='ingredient',y='EU counts')
	for j, count in enumerate(newdf.sort_values(by='EU counts', ascending=False)['EU counts'][:20]):
		plt.text(j-0.25, 1.01*count, '%2.1f%%' %(count/total_num[i]*100))
	plt.title(title[i])
	plt.tight_layout()
	plt.show()
	
#total_count_df.sort_values(by='special counts', ascending=False)[:20].plot.bar(x='ingredient',y='special counts')
#plt.tight_layout()
#plt.show()

#plt.figure(figsize=(7,4))
#total_count_df.sort_values(by='common counts', ascending=False)[:20].plot.bar(x='ingredient',y='common counts')
#plt.tight_layout()
#plt.show()

#plt.figure(figsize=(7,4))
#total_count_df.loc[~total_count_df['ingredient'].str.startswith('ci')].sort_values(by='EU counts', ascending=False)[:20].plot.bar(x='ingredient',y='EU counts')
#plt.tight_layout()
#plt.show()


