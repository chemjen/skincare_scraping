import pandas as pd
import re

subs = pd.read_csv('/Users/jen/Downloads/prohibited_substances_from_cosmetics - COSING_AnnexII_v2.csv')
subs = subs[['Chemical name / INN', 'Identified INGREDIENTS or substances e.g.']]

subs.rename(columns = {'Chemical name / INN':'chem_name', 'Identified INGREDIENTS or substances e.g.': 'idins'}, inplace = True)

subs['chem_name'] = subs['chem_name'].str.lower()
subs['idins'] = subs['idins'].str.lower()

## the following rows of the data are about petroleum and coal byproducts, 
## which can be summed up as paraffin, napthenic compounds, pegs, petrolatum,
## petroleum jelly
subs = subs.loc[~subs['chem_name'].str.contains('petroleum')]
subs = subs[~subs['chem_name'].str.contains('coal tar')]
subs = subs[~subs['chem_name'].str.contains('(coal)')]
subs = subs[~subs['chem_name'].str.contains('hydrocarbon')]
subs = subs.loc[~subs['chem_name'].str.contains('alkane')]
subs = subs.loc[~subs['chem_name'].str.contains('fuel oil')]
subs = subs.loc[~subs['chem_name'].str.contains('gas oil')]
subs = subs.loc[~subs['chem_name'].str.contains('pitch')]
subs = subs.loc[~subs['chem_name'].str.contains('slimes and sludge')]
subs = subs.loc[~subs['chem_name'].str.contains('phenates')]
subs = subs.loc[~subs['chem_name'].isin(['anthracene oil', 'benzene', 'benzo[def]chrysene; (=benzo[a]pyrene) '])]
banned_subs = ['anthracene', 'benzene', 'enzo[def]chrysene', 'benzo[a]pyrene', 'formaldehyde', 'naptha', \
	'naphthalene', 'mineral oil', 'peg', 'petrolatum', 'petroleum jelly', 'phenate']

# no human parts
subs = subs.loc[~subs['chem_name'].str.contains('human')]
banned_subs.append('human')

## fragrance ingredients
fragrances = subs.loc[subs['chem_name'].str.contains('fragrance')]
banned_subs.extend(fragrances.idins.dropna().values.flatten())
fragnames = fragrances.chem_name.values.flatten()
fragnames = [x.split(', when')[0] for x in fragnames]
fragnames = [x.split(' and derivatives')[0] for x in fragnames]
banned_subs.extend(fragnames)

subs = subs.loc[~subs['chem_name'].str.contains('fragrance')]

## hair dye ingredients
#hair_dyes = subs.loc[subs['chem_name'].str.contains('hair dye')]
#hairdyenames = hair_dyes.chem_name.values.flatten()

#postdye=[]
#for hairdye in hairdyenames:
#    cis = re.findall('ci \d\d\d\d\d\)', hairdye)
#    if cis:
#        banned_subs.append(cis[0][:-1])
#        hairdye = hairdye.replace(cis[0],'')
#    colorname = re.findall('\(\w+ \w+ no \d\d?', hairdye)
#    if colorname:
#        banned_subs.append(colorname[0][1:])
#        hairdye = hairdye.replace(colorname[0], '')
#    colorname = re.findall('\(\w+ \w+ \d\d?', hairdye)
#    if colorname:  
#        banned_subs.append(colorname[0][1:])
#        hairdye = hairdye.replace(colorname[0], '') 
#    cas =  re.findall('\(cas \d\d\d\d-\d\d=\d; einecs \d\d\d-\d\d\d-\d\)', hairdye)
#    if cas:
#        hairdye = hairdye.replace(cas, '')
#    postdye.append(hairdye)
#postdye = [(dye.split('when used')[0]).split('and its')[0] for dye in postdye]
#postdye = [(dye.split('reaction products')[0]).split('its')[0] for dye in postdye]
#postdye = [dye.split(', hydroxide')[0] for dye in postdye]
#postdye = [dye.replace('(ponceau sx','').replace('(fast green fcf','').strip().strip(';').strip().strip(' )') for dye in postdye]
#postdye = [dye.strip(',').strip('(').strip(';').strip() for dye in postdye]

#for dye in postdye:
#	nameparts = dye.split(', ')
#	if len(nameparts) > 1:
#		for namepart in nameparts[1:]:
#			banned_subs.append(namepart+nameparts[0])
#	else:
#		banned_subs.append(dye)

#banned_subs.extend(hair_dyes['idins'].values.flatten())

subs = subs.loc[~subs['chem_name'].str.contains('hair dye')]


## other dyes
banned_subs.extend(subs.loc[subs['chem_name'].str.contains('hc ')]['chem_name'].values.flatten())
subs = subs.loc[~subs['chem_name'].str.contains('hc ')]

chem_name = subs['chem_name'].values

CIs = []
for name in chem_name:
	if re.findall('\d\d\d\d\d', name):
		CIs.extend(re.findall('\d\d\d\d\d', name))

## these are more descriptive names than actual chemical names
chem_name = [x for x in chem_name if ('vaccines' not in x) and \
	('category' not in x) and ('narcotics' not in x) and \
	('radioactive' not in x) and ('sympathicomimetic' not in x)]

## chemical names are split by ';' and 'e.g.'
names = []
for name in chem_name:
	names.extend(name.split(';'))

chem_name = []
for name in names:
	chem_name.extend(name.split('e.g'))

## some of the chem_names have 'e.g.' and some have 'e.g' so splitting at 'e.g' results in leftover periods
chem_name = [name.strip('.').strip() for name in chem_name]
chem_name = [((name.split('with the')[0]).split('except')[0]).strip().strip(',').strip() for name in chem_name]
longnames = []

for name in chem_name:
	if len(name) >= 100:
		longnames.append(name)
	else:
		parts = name.split(', ')
		if len(parts) < 2:
			banned_subs.append(name)
		else:
			if (parts[1][-1] == ')') and ('(fruit' not in name) and ('(leaves' not in name) and ('phosphate' not in name):
				banned_subs.extend([parts[0], parts[1].replace('mixed isomers', '')])
			else:
				banned_subs.append(parts[0])

longnames = [name for name in longnames if ('theoretical' not in name) and ('of:' not in name) and ('reaction' not in name)]

for name in longnames:
	if 'ci 42640 (' in name: 
		name = name.split('ci 42640 (')[1].split(', ')[0]
		banned_subs.extend([name, 'ci 42640'])
	elif 'ipecacuanha' in name:
		banned_subs.extend(['cephaelis ipecacuanha brot', 'ipecacuanha'])
	elif 'creosote oil' in name:
		banned_subs.append('creosote oil')
	elif 'borate' in name:
		if len(name.split(':')) > 1:
			name = name.split(':')[1]
		name = name.split(' [')
		names = [name[0]] + [x[2:].split(', ')[0] for x in name[1:]]
	else:
		banned_subs.extend([name])

ingredient = subs['idins'].dropna().values

for item in ingredient:
	if re.findall('\d\d\d\d\d', item):
		CIs.extend(re.findall('\d\d\d\d\d', item))

ingredients = []
for item in ingredient:
	ingredients.extend(item.split(';'))

banned_subs.extend(['coca','erythroxylum coca', 'noretynodrel', 'northynodrel'])

#print(ingredients)
terms = [', with the', ', compound', ', elemen',', ext', ', if', ', mixed']

ingredients_cleaned = []
for ingredient in ingredients:
	for term in terms:
		ingredient = ingredient.split(term)[0]
	ingredients_cleaned.append(ingredient)

for item in ingredients_cleaned[:50]:
	item = re.sub('\(\d:\d\)', '', item)
	item = re.sub('\(\d:\?\)', '', item)
	item = re.sub('\(\?:\d\)', '', item)
	item = re.sub('\(\?:\?\)', '', item)
	item = item.replace('(salt)', '')
	item = item.strip()
	if len(item.split(', ')) < 2:
		banned_subs.extend([item])
	else:
		items = item.split(', ')
		base= items[0]
		extras = items[1:]	
		items = []
		for extra in extras:
			if extra.startswith('di') or extra.startswith('mono') or \
				extra.endswith('ide') or extra.endswith('ite') or extra.endswith('ate'):
				items.append(base+' '+extra)
			elif extra.endswith('-'):
				items.append(extra+base)
			else:
				items.extend([extra+base, base+extra])
		banned_subs.extend(items)
		
banned_subs.extend(['cholecalciferol', 'vitamin d2', 'vitamin d3', 'ergocalciferol'])

banned_subs_cleaned = []

banned_subs = [substance for substance in banned_subs if type(substance) != float]

for substance in banned_subs:
	substance = re.sub('\(\*+\)', '', substance)
	substance = re.sub('\(\d:\d\)', '', substance)
	substance = re.sub('\(\d:\?\)', '', substance)
	substance = substance.lstrip(']')
	substance = substance.split('and its')[0]
	substance = substance.split(' (polym')[0]
	substance = substance.split(' for trace')[0]
	substance = substance.split(' sodium salt')[0]
	substance = substance.split('/sodium salt')[0]
	substance = substance.replace('(usan:ban:jan)','').replace('(usan:ban:jan)','')
	substance = substance.replace('[usan:jan]','')
	substance = substance.strip('(+/-)-').strip('(+/-) ').strip()
	substance = substance.replace('- ','-').replace(' -','-')
	if substance.startswith('[') and substance.endswith(']'):
		substance.lstrip('[').rstrip(']')
	if substance.startswith('(') and substance.endswith(')'):
		substance.lstrip('(') and substance.rstrip(')')

	if len(re.findall(' \([A-Za-z0-9 \-]+\)$', substance)) > 0:
		altname = re.findall(' \([A-Za-z0-9 \-]+\)$', substance)[0][2:-1]
		substance = re.sub(' \([A-Za-z0-9 \-]+\)$', '', substance)
	elif len(re.findall(' \([A-Za-z0-9 \-]+$', substance)) > 0:
		altname = re.findall(' \([A-Za-z0-9 \-]+$', substance)[0][2:]
		substance = re.sub(' \([A-Za-z0-9 \-]+$', '', substance)
	elif len(re.findall(' \([A-Za-z0-9 \-\(\)]+\)$', substance)):
		altname = re.findall(' \([A-Za-z0-9 \-\(\)]+\)$', substance)[0][2:-1]
		substance = re.sub(' \([A-Za-z0-9 \-\(\)]+\)$', '', substance)
	elif len(re.findall(' \([A-Za-z0-9 \-\(\)]+$', substance)):
		altname = re.findall(' \([A-Za-z0-9 \-\(\)]+$', substance)[0][2:]
		substance = re.sub(' \([A-Za-z0-9 \-\(\)]+$', '',substance)
	else:
		altname = ''
	altname = altname.replace('inn','').replace('- iso','').replace('iso','')
	if altname in ['stabilized', 'oil', 'fruit', 'essential oil', 'leaves']: altname = ''
	if 'cas no' in altname: altname = ''
	if len(altname) > 0:
		banned_subs_cleaned.append(altname)

	substance = re.sub(' \[\d+\]$', '', substance)
	substance = re.sub('\(\w{3,4}\)', '', substance)
	substance = re.sub('\[\w{3,4}\]', '', substance)
	banned_subs_cleaned.append(substance)

	if len(substance.split(' (')) == 2:
		if len(substance.split(' (')[0]) > 10:
			banned_subs_cleaned.extend(substance.split(' ('))

ci_nums = []
for substance in banned_subs_cleaned:
	if re.findall('\d\d\d\d\d', substance):
		ci_nums.append(re.findall('\d\d\d\d\d', substance)[0]) 

banned_subs_cleaned.extend(ci_nums)


banned_subs_cleaned = list(set(banned_subs_cleaned))
with open('banned_substances3.txt', 'w') as f:
	for substance in banned_subs_cleaned:
		f.write(substance+'\n')


with open('CIs.txt', 'w') as f:
	for ci in CIs:
		f.write(ci+'\n')



#    substance = substance.replace('c.i. ','').strip()
#    substance = substance.replace(' -', '-')

#    altname = re.findall(' \([A-Za-z0-9 \-]+\)$', substance)
#    if altname:
#        if altname in [' (coal)', ' (inn)', ' (fruit)', ' (oil)', ' (usan)', ' (stabilized)']:
#            firstname = substance.split(altname[0])[0].strip()
#            substances_cleaned.extend([firstname])
#        else:
#            firstname = substance.split(altname[0])[0].strip()
#            if 'iso' in altname[0]:
#                altname = altname[0].strip('- iso)')[2:]	
#            else:
#                altname = altname[0][2:-1]
#            substances_cleaned.extend([firstname, altname])
#    elif ('sympathicomimetic' in substance) or ('human' in substance):
#        continue
#    elif len(substance) == 0: 
#        pass
#    elif len(substance.split('/')) > 1:
#        substance = substance.split('/')
#    else:
#        substances_cleaned.extend([substance])
#
#print(substances_cleaned)

#substances_cleaned.extend(['human', 'petroleum', 'coal', 'tar', 'benzene', '1,3-butadiene',
#	 'naptha', 'napthalene', 'formaldehyde', 'triphenyl phosphate', 'petrolatum', 'paraffin',
#	'mineral oil', 'paraben', 'propyl paraben', 'fragrance', 'hydroquinone', 'phthalate',
#	'p-phenylenediamene',  'oxybenzone', 'avobenzone', 'dioxane', 'peg'])

#print(len(list(set(substances_cleaned))))

#substances_cleaned = list(set(substances_cleaned))

#with open('banned_substances.txt', 'w') as f:
#	for substance in substances_cleaned:
#		f.write(substance+'\n')




