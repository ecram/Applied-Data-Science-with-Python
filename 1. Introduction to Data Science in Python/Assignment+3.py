
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[11]:

import pandas as pd
import numpy as np
import re

# Load the Energy Excel sheet into Panda Dataframe
energy = pd.ExcelFile('Energy Indicators.xls')
energy = energy.parse('Energy', skiprows=17, skip_footer=38)
# Delete the first two columns and the index 0 (sub-columns)
del energy['Unnamed: 0']
del energy['Unnamed: 1']
a = energy.iloc[3]['Petajoules']
# Rename the columns name
new_cols = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy.rename(columns=dict(zip(energy.columns[0:], new_cols)),inplace=True)
# Replace '...' with np.nan type & and multiply the 'Energy Supply' column by 1.000.000
#energy = energy.drop(energy.index[0])
energy = energy.replace(a, np.nan)
energy['Energy Supply'] *= 1000000
# Remove parenthesis and numbes and rename the following list of countries
energy['Country'] = energy['Country'].map(lambda x: x.rstrip('1234567890'))
energy['Country'] = energy['Country'].apply(lambda x: re.sub(r" \(.*\)", "", x))
#energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
energy['Country'] = energy['Country'].replace("Republic of Korea","South Korea")
energy['Country'] = energy['Country'].replace("United States of America","United States")
energy['Country'] = energy['Country'].replace("United Kingdom of Great Britain and Northern Ireland",
                                              "United Kingdom")
energy['Country'] = energy['Country'].replace("China, Hong Kong Special Administrative Region","Hong Kong")
# Set Country column to be the index
#energy = energy.set_index(['Country'])

# ----------------------------------------------------

# Load the 'world_bank.csv' sheet into Panda Dataframe
GDP = pd.read_csv('world_bank.csv',skiprows=4)
# Rename the 'Country Name' col by 'Countr'
GDP = GDP.rename(columns = {'Country Name':'Country'})
# Select the last 10 years (2006-2015) of GDP data
GDP = GDP[['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
# Rename the following list of countries
GDP['Country'] = GDP['Country'].replace({"Korea, Rep.": "South Korea","Iran, Islamic Rep.": "Iran",                                         "Hong Kong SAR, China": "Hong Kong"})
# Set Country column to be the index
#GDP = GDP.set_index(['Country'])

# ----------------------------------------------------

# Load the 'scimagojr.xlsx' sheet into Panda Dataframe
ScimEn = pd.ExcelFile('scimagojr-3.xlsx')
ScimEn = ScimEn.parse('Sheet1', skip_footer=176)
# Set Country column to be the index
#ScimEn = ScimEn.set_index(['Country'])

#energy.to_csv('teste.csv')
#GDP.to_csv('teste2.csv')
#print(energy.index)
#print(energy.columns)
#print(energy.head())
#print(ScimEn.head())
#GDP.head()
ScimEn2 = pd.ExcelFile('scimagojr-3.xlsx')
ScimEn2 = ScimEn2.parse('Sheet1')

# ----------------------------------------------------

def answer_one():
    # Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names).
    new_pd = pd.merge(pd.merge(ScimEn,energy,on='Country'),GDP,on='Country')
    # Set Country column to be the index
    new_pd = new_pd.set_index(['Country'])
    return new_pd

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[1]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[10]:

# Copy the energy Panda Dataframe
energy2 = energy.copy()

# ----------------------------------------------------

# Load the 'world_bank.csv' sheet into Panda Dataframe
GDP2 = GDP.copy()

# ----------------------------------------------------

# G = len of Merge(energy2, GDP2, ScimEn2)
# D = len of Merge_inner (energy2, GDP2) - G
# E = len of Merge_inner (energy2, ScimEn2) - G
# F = len of Merge_inner (GDP2, ScimEn2) - G
# A = A - D - G - E
# B = B - D - G - F
# C = C - E - G - F

merge3 = pd.merge(pd.merge(energy2,GDP2,on='Country'),ScimEn2,on='Country')
inner_energy2_GDP2 = pd.merge(energy2, GDP2, how='inner', left_on='Country', right_on='Country')
inner_energy2_ScimEn2 = pd.merge(energy2, ScimEn2, how='inner', left_on='Country', right_on='Country')
inner_GDP2_ScimEn2 = pd.merge(GDP2, ScimEn2, how='inner', left_on='Country', right_on='Country')

def answer_two():
    G = len(merge3)
    D = len(inner_energy2_GDP2) - G
    E = len(inner_energy2_ScimEn2) - G
    F = len(inner_GDP2_ScimEn2) - G
    A = len(energy2) - D - G - E
    B = len(GDP2) - D - G - F
    C = len(ScimEn2) - E - G - F
    R = A + B + C + D + E + F
    return R
answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[12]:

def answer_three():
    Top15 = answer_one()
    # The average GDP over the last 10 years for each of 15 countries using mean(axis=1) and Rename name
    avgGDP = Top15[['2006','2007','2008','2009','2010','2011','2012','2013',
                    '2014','2015']].mean(axis=1).rename('avgGDP').sort_values(ascending=False)
    # Rename the columns name
    #avgGDP.columns = ['Country','avgGDP']
    return avgGDP
answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[20]:

def answer_four():
    Top15 = answer_one()
    #resp = Top15[Top15['Rank'] == 4]['2015'] - Top15[Top15['Rank'] == 4]['2006']
    resp = Top15.iloc[3]['2015'] - Top15.iloc[3]['2006']
    return resp
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[24]:

def answer_five():
    Top15 = answer_one()
    resp = Top15[['Energy Supply per Capita']].mean()
    return float(resp[0])
answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[22]:

def answer_six():
    Top15 = answer_one()
    # resp = Top15[Top15['% Renewable'] == max(Top15['% Renewable'])]
    # Sort the list in descending order
    Top15.sort_values('% Renewable',ascending=False,inplace=True)
    resp6 = (Top15.iloc[0].name,Top15.iloc[0]['% Renewable'])
    return resp6
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[25]:

def answer_seven():
    Top15 = answer_one()
    Top15['Radio Citations'] = Top15['Self-citations'] / Top15['Citations']
    Top15.sort_values('Radio Citations', ascending=False, inplace=True)
    resp7 = (Top15.iloc[0].name, Top15.iloc[0]['Radio Citations'])
    return resp7
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[26]:

def answer_eight():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply'] / (Top15['Energy Supply per Capita'] * 1000000)
    Top15.sort_values('Population', ascending=False, inplace=True)
    resp8 = Top15.iloc[2].name
    return resp8
answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[27]:

def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    resp9 = Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
    return resp9
answer_nine()


# In[29]:

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[30]:

#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[31]:

def answer_ten():
    Top15 = answer_one()
    median = Top15['% Renewable'].median()
    Top15['HighRenew'] = [1 if x >= median else 0 for x in Top15['% Renewable']]
    return Top15['HighRenew']
answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[32]:

def answer_eleven():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).astype(float)
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    # Map ContinentDict by country 
    Top15 = Top15.reset_index()
    #Top15['Continent'] = [ContinentDict[country] for country in Top15['Country']]
    Top15['Continent'] = Top15['Country'].map(ContinentDict)
    # Calculate each column value
    Top15_size = Top15.groupby('Continent').agg({'Continent':np.count_nonzero})
    Top15_sum = Top15.groupby('Continent').agg({'PopEst':np.sum})
    Top15_mean = Top15.groupby('Continent').agg({'PopEst':np.average})
    Top15_std = Top15.groupby('Continent').agg({'PopEst':np.std})
    # Concatenate the values in a new table with name columns
    resp11 = pd.concat([Top15_size, Top15_sum, Top15_mean, Top15_std],axis=1)
    resp11.columns = ['size', 'sum', 'mean', 'std']
    return resp11
answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[34]:

def answer_twelve():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    # Map ContinentDict by country 
    Top15 = Top15.reset_index()
    Top15['Continent'] = Top15['Country'].map(ContinentDict)
    # Cut in 5 bins by '% Renewable'
    Top15['5 bins'] = pd.cut(Top15['% Renewable'],5)
    return Top15.groupby(['Continent','5 bins']).size()
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[35]:

def answer_thirteen():
    Top15 = answer_one()
    # Obtain the estimated population
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    # Use format to thousands separator (using commas)
    Top15['PopEst'] = Top15['PopEst'].apply(lambda x : '{:,}'.format(x))
    # Convert of float to string
    resp13 = (Top15['PopEst']).astype(str)
    return resp13
answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[39]:

def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[40]:

#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!


# In[ ]:



