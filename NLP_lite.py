import matplotlib.pyplot as plt
from collections import Counter
import nltk
import pandas as pd
import re
from textblob import TextBlob

df = pd.read_csv('sephora_clean.csv')
df['details'] = df['details'].str.lower()
dets = df[['family', 'brand', 'name', 'details']].dropna()
menskincare = df.loc[(df['family']=='Men') & (df['genus'] == 'Skincare')]
menskincare = menskincare[['family', 'brand', 'name', 'details']].dropna()
skincare = dets.loc[dets['family'] == 'Skincare']
generic_phrases = ['what it is', 'which skin type is it good for?', 'ingredient callouts',
	'what is it good for', 'highlighted ingredients', 
	'formulation', 'skin type', 'what it is formulated without', 'skincare concerns',
	'solutions for', 'what else you need to know']

skincare['details'] = skincare['details'].apply(lambda x: x.split('clean at sephora')[0])
menskincare['details'] = menskincare['details'].apply(lambda x: x.split('clean at sephora')[0])

for phrase in generic_phrases:
	skincare['details'] = skincare['details'].apply(lambda x: x.replace(phrase, ' '))
	menskincare['details'] = menskincare['details'].apply(lambda x: x.replace(phrase, ' '))

skincare['details'] = skincare['details'].apply(lambda x: x.replace('\\n', ' '))
skincare['details'] = skincare['details'].apply(lambda x: re.sub('\s+', ' ', x))
skincare['details'] = skincare['details'].apply(lambda x: re.sub('[^\w\s]', '', x))

menskincare['details'] = menskincare['details'].apply(lambda x: x.replace('\\n', ' '))
menskincare['details'] = menskincare['details'].apply(lambda x: re.sub('\s+', ' ', x))
menskincare['details'] = menskincare['details'].apply(lambda x: re.sub('[^\w\s]', '', x))

from nltk.corpus import stopwords
stop = stopwords.words('english')

skincare['details'] = skincare['details'].apply(lambda text: " ".join(word for word in text.split() if word not in stop))
menskincare['details'] = menskincare['details'].apply(lambda text: " ".join(word for word in text.split() if word not in stop))
#from nltk import WordNetLemmatizer
#lemztr = WordNetLemmatizer()

details = skincare['details'].values.flatten()
bigrams = []
for detail in details:
	bigrams.extend(TextBlob(detail).ngrams(2))

total_bigrams = len(bigrams)
bigram_counts = Counter(str(bigram) for bigram in bigrams)  
bigram_counts = pd.DataFrame(list(bigram_counts.items()), columns=['bigram', 'count'])
bigram_counts['bigram'] = bigram_counts['bigram'].apply(lambda x: ' '.join(''.join(list(x)[1:-1]).strip("'").split("', '")))
bigram_counts.sort_values(by='count', ascending=False)[:30].plot.bar(x='bigram', y='count')
plt.tight_layout()
plt.show()


trigrams = []
for detail in details:
    trigrams.extend(TextBlob(detail).ngrams(3))

total_trigrams = len(trigrams)
trigram_counts = Counter(str(trigram) for trigram in trigrams)
trigram_counts = pd.DataFrame(list(trigram_counts.items()), columns=['trigram', 'count'])
trigram_counts['trigram'] = trigram_counts['trigram'].apply(lambda x: ' '.join(''.join(list(x)[1:-1]).strip("'").split("', '")))
trigram_counts.sort_values(by='count', ascending=False)[:17].plot.bar(x='trigram', y='count')
plt.tight_layout()
plt.show()

details = menskincare['details'].values.flatten()
bigrams = []
for detail in details:
	bigrams.extend(TextBlob(detail).ngrams(2))

total_bigrams = len(bigrams)
bigram_counts = Counter(str(bigram) for bigram in bigrams)  
bigram_counts = pd.DataFrame(list(bigram_counts.items()), columns=['bigram', 'count'])
bigram_counts['bigram'] = bigram_counts['bigram'].apply(lambda x: ' '.join(''.join(list(x)[1:-1]).strip("'").split("', '")))
bigram_counts.sort_values(by='count', ascending=False)[:30].plot.bar(x='bigram', y='count')
plt.tight_layout()
plt.show()


trigrams = []
for detail in details:
    trigrams.extend(TextBlob(detail).ngrams(3))

total_trigrams = len(trigrams)
trigram_counts = Counter(str(trigram) for trigram in trigrams)
trigram_counts = pd.DataFrame(list(trigram_counts.items()), columns=['trigram', 'count'])
trigram_counts['trigram'] = trigram_counts['trigram'].apply(lambda x: ' '.join(''.join(list(x)[1:-1]).strip("'").split("', '")))
trigram_counts.sort_values(by='count', ascending=False)[:17].plot.bar(x='trigram', y='count')
plt.tight_layout()
plt.show()






#from wordcloud import WordCloud
#wc = WordCloud(background_color="white", max_words=1000, width=800, height=400)
#wc.generate(' '.join(skincare['details']))
#import matplotlib.pyplot as plt
#plt.figure(figsize=(12, 6))
#plt.imshow(wc, interpolation='bilinear')
#plt.axis("off")
#plt.show()
#d = defaultdict(int) #values will be integers. can also be list or string, etc
#for s in day_i:
 #   cust, order = s.split(':') 
  #  d[cust] += int(order)







