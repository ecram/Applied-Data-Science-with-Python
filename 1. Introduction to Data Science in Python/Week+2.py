
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # The Series Data Structure

# In[1]:

import pandas as pd
get_ipython().magic('pinfo pd.Series')


# In[2]:

animals = ['Tiger', 'Bear', 'Moose']
pd.Series(animals)


# In[3]:

numbers = [1, 2, 3]
pd.Series(numbers)


# In[4]:

animals = ['Tiger', 'Bear', None]
pd.Series(animals)


# In[5]:

numbers = [1, 2, None]
pd.Series(numbers)


# In[6]:

import numpy as np
np.nan == None


# In[7]:

np.nan == np.nan


# In[8]:

np.isnan(np.nan)


# In[9]:

sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports)
s


# In[10]:

s.index


# In[11]:

s = pd.Series(['Tiger', 'Bear', 'Moose'], index=['India', 'America', 'Canada'])
s


# In[12]:

sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports, index=['Golf', 'Sumo', 'Hockey'])
s


# # Querying a Series

# In[13]:

sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports)
s


# In[14]:

s.iloc[3]


# In[15]:

s.loc['Golf']


# In[16]:

s[3]


# In[17]:

s['Golf']


# In[18]:

sports = {99: 'Bhutan',
          100: 'Scotland',
          101: 'Japan',
          102: 'South Korea'}
s = pd.Series(sports)


# In[19]:

s[0] #This won't call s.iloc[0] as one might expect, it generates an error instead


# In[20]:

s = pd.Series([100.00, 120.00, 101.00, 3.00])
s


# In[21]:

total = 0
for item in s:
    total+=item
print(total)


# In[22]:

import numpy as np

total = np.sum(s)
print(total)


# In[23]:

#this creates a big series of random numbers
s = pd.Series(np.random.randint(0,1000,10000))
s.head()


# In[24]:

len(s)


# In[27]:

get_ipython().run_cell_magic('timeit', '-n 100', 'summary = 0\nfor item in s:\n    summary+=item')


# In[31]:

get_ipython().run_cell_magic('timeit', '-n 100', 'summary = np.sum(s)')


# In[32]:

s+=2 #adds two to each item in s using broadcasting
s.head()


# In[33]:

for label, value in s.iteritems():
    s.set_value(label, value+2)
s.head()


# In[34]:

get_ipython().run_cell_magic('timeit', '-n 10', 's = pd.Series(np.random.randint(0,1000,10000))\nfor label, value in s.iteritems():\n    s.loc[label]= value+2')


# In[35]:

get_ipython().run_cell_magic('timeit', '-n 10', 's = pd.Series(np.random.randint(0,1000,10000))\ns+=2')


# In[36]:

s = pd.Series([1, 2, 3])
s.loc['Animal'] = 'Bears'
s


# In[37]:

original_sports = pd.Series({'Archery': 'Bhutan',
                             'Golf': 'Scotland',
                             'Sumo': 'Japan',
                             'Taekwondo': 'South Korea'})
cricket_loving_countries = pd.Series(['Australia',
                                      'Barbados',
                                      'Pakistan',
                                      'England'], 
                                   index=['Cricket',
                                          'Cricket',
                                          'Cricket',
                                          'Cricket'])
all_countries = original_sports.append(cricket_loving_countries)


# In[38]:

original_sports


# In[39]:

cricket_loving_countries


# In[40]:

all_countries


# In[41]:

all_countries.loc['Cricket']


# # The DataFrame Data Structure

# In[45]:

import pandas as pd
purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})
df = pd.DataFrame([purchase_1, purchase_2, purchase_3], index=['Store 1', 'Store 1', 'Store 2'])
df.head()


# In[46]:

df.loc['Store 2']


# In[47]:

type(df.loc['Store 2'])


# In[48]:

df.loc['Store 1']


# In[49]:

df.loc['Store 1', 'Cost']


# In[50]:

df.T


# In[51]:

df.T.loc['Cost']


# In[52]:

df['Cost']


# In[53]:

df.loc['Store 1']['Cost']


# In[54]:

df.loc[:,['Name', 'Cost']]


# In[59]:

df.drop('Store 1')


# In[60]:

df


# In[61]:

copy_df = df.copy()
copy_df = copy_df.drop('Store 1')
copy_df


# In[62]:

get_ipython().magic('pinfo copy_df.drop')


# In[63]:

del copy_df['Name']
copy_df


# In[64]:

df['Location'] = None
df


# # Dataframe Indexing and Loading

# In[65]:

costs = df['Cost']
costs


# In[66]:

costs+=2
costs


# In[67]:

df


# In[68]:

get_ipython().system('cat olympics.csv')


# In[135]:

df = pd.read_csv('olympics.csv')
df.head()


# In[136]:

df = pd.read_csv('olympics.csv', index_col = 0, skiprows=1)
df.head()


# In[137]:

df.columns


# In[138]:

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold' + col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver' + col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze' + col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#' + col[1:]}, inplace=True) 

df.head()


# # Querying a DataFrame

# In[139]:

df['Gold'] > 0


# In[140]:

only_gold = df.where(df['Gold'] > 0)
only_gold.head()


# In[141]:

only_gold['Gold'].count()


# In[142]:

df['Gold'].count()


# In[143]:

only_gold = only_gold.dropna()
only_gold.head()


# In[144]:

only_gold = df[df['Gold'] > 0]
only_gold.head()


# In[145]:

len(df[(df['Gold'] > 0) | (df['Gold.1'] > 0)])


# In[146]:

df[(df['Gold.1'] > 0) & (df['Gold'] == 0)]


# In[155]:

df.loc[df['Gold'].idxmax()]


# In[167]:

#df = df.drop('Totals')
def answer_two():
    df['dif'] = abs(df['Total']-df['Total.1'])
    return df['dif'].idxmax()
answer_two()
df.sort_values('dif',ascending = False).head()


# In[182]:

def answer_three():
    new_df =  df[(df['Gold.1'] > 0) & (df['Gold'] > 0)]
    #new_df =  df.where((df['Gold.1'] > 0) & (df['Gold'] > 0))
    new_df['dif2'] = abs(new_df['Total'] - new_df['Total.1']) / new_df['Combined total']
    #print (new_df.sort_values('dif2', ascending = False).head)
    return new_df['dif2'].idxmax()
answer_three()
#df2.sort_values('dif2',ascending = False)


# In[198]:

def answer_four():
    #new_df['Points'] = pd.Series((df['Gold.2']*3) + (df['Silver.2']*2) + (df['Bronze.2']*2), name = 'Points')
    df['Points'] = (df['Gold.2']*3) + (df['Silver.2']*2) + (df['Bronze.2'])
    return df['Points']
answer_four().head()


# # Indexing Dataframes

# In[82]:

df.head()


# In[85]:

df['country'] = df.index
df = df.set_index('Gold')
df.head()


# In[86]:

df = df.reset_index()
df.head()


# In[271]:

census_df = pd.read_csv('census.csv')
census_df.head()


# In[337]:

new_df = census_df.groupby(['STNAME']).size().reset_index(name='count')
new_df = new_df.reset_index()
new_df = new_df.set_index(['STNAME'])
del new_df['index']
new_df.sort_values('count', ascending=False).head()


# In[376]:

new_df['3pop2010'] = 0
new_df['COUNTIES'] = 0
new_df.head()


# In[377]:

new_sdf = census_df[['STNAME','CENSUS2010POP']].copy()
new_sdf = new_sdf.sort_values(['STNAME','CENSUS2010POP'], ascending=False)
new_sdf = new_sdf.reset_index()
new_sdf = new_sdf.set_index(['STNAME'])
del new_sdf['index']

new_sdf.head()


# In[386]:

for st, ndf in new_df.iterrows():
    for st2, nsdf in new_sdf.iterrows():
        if st == st2 and ndf['COUNTIES'] < 3:
            ndf['3pop2010'] += nsdf['CENSUS2010POP']
            ndf['COUNTIES'] += 1

pop3 = new_df.sort_values('3pop2010', ascending=False).head()


# In[399]:

pop3.head()
lista = []
lista = pop3.index[0:3].tolist()
print(lista)


#print(lista[0]+' - '+lista[1]+' - '+lista[2])


# In[ ]:

### Question 7
Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)

e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.

*This function should return a single string value.*


# In[428]:

df7 = census_df[['CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']].copy()
df7 = df7.reset_index()
df7 = df7.set_index(['CTYNAME'])
del df7['index']

df7['dif'] = 0

max_df7 = df7[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']].max(axis=1)
min_df7 = df7[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']].min(axis=1)

df7['dif'] = max_df7 - min_df7

df7.sort_values('dif', ascending=False).index[0]


# In[ ]:

En este archivo de datos, los Estados Unidos se dividen en cuatro regiones utilizando la columna "REGIÓN".

Cree una consulta que encuentre los condados que pertenecen a las regiones 1 o 2, cuyo nombre comienza con 
'Washington' y cuyo POPESTIMATE2015 fue mayor que su POPESTIMATE 2014.

Esta función debe devolver un DataFrame de 5x2 con las columnas = ['STNAME', 'CTYNAME'] y el mismo ID de índice 
que census_df (ordenado ascendente por índice).


# In[485]:

census_df = pd.read_csv('census.csv')
census_df.head()


# In[486]:

df8 = census_df[((census_df['REGION'] == 1) | (census_df['REGION'] == 2)) 
                & (census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014'])]

df8.head()


# In[493]:

df8 = df8[df8['CTYNAME'].str.startswith('Washington')].copy()
sol = df8[['STNAME', 'CTYNAME']].copy()
sol


# In[472]:

aux = census_df[census_df['CTYNAME'].str.match('Washington')]
#df8 = df8[['STNAME', 'CTYNAME']].copy()
aux


# In[209]:

df['SUMLEV'].unique()


# In[90]:

df=df[df['SUMLEV'] == 50]
df.head()


# In[91]:

columns_to_keep = ['STNAME',
                   'CTYNAME',
                   'BIRTHS2010',
                   'BIRTHS2011',
                   'BIRTHS2012',
                   'BIRTHS2013',
                   'BIRTHS2014',
                   'BIRTHS2015',
                   'POPESTIMATE2010',
                   'POPESTIMATE2011',
                   'POPESTIMATE2012',
                   'POPESTIMATE2013',
                   'POPESTIMATE2014',
                   'POPESTIMATE2015']
df = df[columns_to_keep]
df.head()


# In[92]:

df = df.set_index(['STNAME', 'CTYNAME'])
df.head()


# In[93]:

df.loc['Michigan', 'Washtenaw County']


# In[94]:

df.loc[ [('Michigan', 'Washtenaw County'),
         ('Michigan', 'Wayne County')] ]


# In[123]:

purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})

df2 = pd.DataFrame([purchase_1, purchase_2, purchase_3], index=['Store 1', 'Store 1', 'Store 2'])
df3 = df2.copy()

df2


# In[124]:

df2['Location'] = df2.index
df2 = df2.set_index(['Location','Name'])
otros = pd.Series(data = {'Cost':3.00,'Item Purchased':'Kitty Food'},name=('Store 2','Kevyn'))
df2 = df2.append(otros)
df2


# In[125]:

df3 = df3.set_index([df3.index, 'Name'])
df3.index.names = ['Location', 'Name']
df3 = df3.append(pd.Series(data={'Cost': 3.00, 'Item Purchased': 'Kitty Food'}, name=('Store 2', 'Kevyn')))
df3


# # Missing values

# In[126]:

df = pd.read_csv('log.csv')
df


# In[127]:

get_ipython().magic('pinfo df.fillna')


# In[128]:

df = df.set_index('time')
df = df.sort_index()
df


# In[132]:

df = df.reset_index()
df = df.set_index(['time', 'user'])
df2 = df.copy()
df


# In[133]:

df = df.fillna(method='ffill')
df.head()


# In[134]:

df2


# In[ ]:



