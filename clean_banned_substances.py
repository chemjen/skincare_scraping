import pandas as pd

subs = pd.read_csv('/Users/jen/Downloads/prohibited_substances_from_cosmetics - COSING_AnnexII_v2.csv')
rawr.columns
rawr['Chemical name / INN']
INNs = rawr.loc[rawr['Chemical name / INN'].str.contains('INN')]
INNS['Chemical name / INN']
INNs['Chemical name / INN']
INNs['Chemical name / INN'].values
INNs['Chemical name / INN'][100]
INNs = INNs['Chemical name / INN'].values.flatten()
INNs[0]
import re
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        print(inns)
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        pass
        #print(inns)
    elif INN.contains('e.g.')
         print(INN)
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        pass
        #print(inns)
    elif INN.contains('e.g.'):
         print(INN)
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        pass
        #print(inns)
    elif 'e.g.' in INN
         print(INN)
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        pass
        #print(inns)
    elif 'e.g.' in INN:
         print(INN)
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        pass
        #print(inns)
    elif 'e.g.' in INN:
        pass
        # print(INN)
    else:
        print(INN)
bb = []
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        bb.extend([inns[0][1:-4]])
        pass
        #print(inns)
    elif 'e.g.' in INN:
        pass
        # print(INN)
    else:
        print(INN)
bb
bb = []
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        bb.extend([inns[0][1:-7]])
    elif 'e.g.' in INN:
        print(INN.split('e.g')[1][:-6])
        # print(INN)
    else:
       # print(INN)
        pass
bb = []
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        bb.extend([inns[0][1:-7]])
    elif 'e.g.' in INN:
        INN = INN.split('e.g')[1][:-6]
        INN = INN.split(' (INN)')[0]
        print(INN)
    else:
       # print(INN)
        pass
bb = []
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        bb.extend([inns[0][1:-7]])
    elif 'e.g.' in INN:
        INN = INN.split('e.g. ')[1][:-6]
        INN = INN.split(' (INN)')[0]
        bb.extend([INN])
    elif 'INCI' in INN:
        INN = INN.split('INCI')
        INN = INN.split(' [INCI], ')
        bb.extend([INN[0], INN[1][:-6]])
    elif 'padimate A' in INN:
        bb.extend(['padimate A'])
        bb.extend(['Cholecalciferol'])
    else:
        bb.extend([INN.split(' (INN)')[0]])
bb = []
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        bb.extend([inns[0][1:-7]])
    elif 'e.g.' in INN:
        INN = INN.split('e.g. ')[1][:-6]
        INN = INN.split(' (INN)')[0]
        bb.extend([INN])
    elif 'INCI' in INN:
        INN = INN.split(' [INCI], ')
        bb.extend([INN[0], INN[1][:-6]])
    elif 'padimate A' in INN:
        bb.extend(['padimate A'])
        bb.extend(['Cholecalciferol'])
    else:
        bb.extend([INN.split(' (INN)')[0]])
bb
bb = []
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        bb.extend([inns[0][1:-7]])
    elif 'e.g.' in INN:
        INN = INN.split('e.g. ')[1][:-6]
        INN = INN.split(' (INN)')[0]
        bb.extend([INN])
    elif 'INCI' in INN:
        INN = INN.split(' [INCI], ')
        bb.extend([INN[0], INN[1][:-6]])
    elif 'Padimate A' in INN:
        bb.extend(['Padimate A'])
        bb.extend(['Cholecalciferol'])
    else:
        bb.extend([INN.split(' (INN)')[0]])
bb
bb = []
for INN in INNs:
    inns = re.findall('\([a-zA-Z0-9_]+ \(INN\)\)', INN)
    if inns:
        bb.extend([inns[0][1:-7]])
    elif 'e.g.' in INN:
        INN = INN.split('e.g. ')[1][:-6]
        INN = INN.split(' (INN)')[0]
        bb.extend([INN])
    elif 'INCI' in INN:
        INN = INN.split(' [INCI], ')
        bb.extend([INN[0], INN[1][:-6]])
    elif 'Padimate A' in INN:
        bb.extend(['Padimate A'])
        bb.extend(['Cholecalciferol'])
    else:
        bb.extend([INN.split(' (INN)')[0]])
for b in bb:
    if (INNM) in b:
        b = b.split(' (INNM)')[0]
for b in bb:
    if '(INNM)' in b:
        b = b.split(' (INNM)')[0]
bb
for i, b in enumerate(bb):
    if '(INNM)' in b:
        bb[i] = b.split(' (INNM)')[0]
bb
history
rawr.columns
rawr = rawr[['Chemical name / INN', 'Identified INGREDIENTS or substances e.g.']]
rawr.head()
rawr.head(50)
rawr = rawr.dropna()
rawr.head(50)
rawr = pd.read_csv('/Users/jen/Downloads/prohibited_substances_from_cosmetics - COSING_AnnexII_v2.csv')
notINNs = rawr.loc[~rawr['Chemical name / INN'].str.contains('INN')]
notINNs['Chemical name / INN'].values
notINNs['Chemical name / INN'].values.flatten()
notINNs.loc[notINNs.loc['Identified INGREDIENTS or substances e.g.'] == np.nan]
notINNs.loc[notINNs['Identified INGREDIENTS or substances e.g.'] == np.nan]
notINNs['Chemical name / INN'].values.flatten()
notINNs = notINNs['Chemical name / INN'].values.flatten()
notINNs
len(notINNs)
notINNs[:100]
notINNs = rawr.loc[~rawr['Chemical name / INN'].str.contains('INN')]
notINNs = notINNs[['Chemical name / INN', 'Identified INGREDIENTS or substances e.g.']]
notINNs.sample(50)
bc = []
colors = notINNs.loc[notINNs['Identified INGREDIENTS or substances e.g.'].str.contains('HC')]
colors = notINNs.loc[notINNs['Identified INGREDIENTS or substances e.g.'].isin(['HC'])]
colors
colors = notINNs.dropna()
colors = colors.loc[notINNs['Identified INGREDIENTS or substances e.g.'].str.contains('HC')]
colors
colors.isnull().sum()
colors = colors.loc[colors['Identified INGREDIENTS or substances e.g.'].str.contains('HC')]
colors
colors = colors.loc[colors['Identified INGREDIENTS or substances e.g.'].str.contains('HC') & colors['Identified INGREDIENTS or substances e.g.'].apply(lambda x: 'HCL' not in x)]
colors
colors = colors.loc[colors['Identified INGREDIENTS or substances e.g.'].str.contains('HC') & colors['Identified INGREDIENTS or substances e.g.'].apply(lambda x: ('HCL' not in x) and ('HCl' not in x))]
colors
colors = colors.loc[colors['Identified INGREDIENTS or substances e.g.'].str.contains('HC ')]
colors
bb.extend(colors['Identified INGREDIENTS or substances e.g.'].values.flatten())
matched = notINNs.dropna()
NOTINNs = notINNs.loc[notINNs['Identified INGREDIENTS or substances e.g.'].isnull()]
NOTINNs
matched
history

