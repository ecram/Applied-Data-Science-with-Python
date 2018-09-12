
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[8]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[9]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[38]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    #Create a list to take state and town
    state_town = []
    # Try to load "university_towns.txt" line by line, applied the cleaning needs
    with open("university_towns.txt") as file:
        for line in file:
            new_line = line[:-1]
            if new_line[-6:] == '[edit]':
                state = new_line[:-6]
            elif "(" in new_line:
                town = new_line[:new_line.index("(")-1]
                state_town.append([state,town])
            else:
                town = new_line
                state_town.append([state,town])
        #print(state_town)
        state_university_town = pd.DataFrame(state_town,columns = ['State','RegionName'])
    return state_university_town
get_list_of_university_towns()


# In[41]:

# Load the 'world_bank.csv' sheet into Panda Dataframe
data = pd.ExcelFile('gdplev.xls')
data = data.parse('Sheet1', skiprows=5)
# Rename the columns that will be used
data.rename(columns = {'Unnamed: 4':'Year by quarter', 
                               'GDP in billions of chained 2009 dollars.1':'GDP'}, inplace=True)
# Select the columns that will be used {Year by quarter, GDP}
gdp_usa_2000 = data[['Year by quarter','GDP']]
# Select columns in gdp_usa_2000[2000q1:...]
gdp_usa_2000 = gdp_usa_2000[214:]
# Convert 'GDP' columns data to float type
gdp_usa_2000['GDP'] = gdp_usa_2000['GDP'].astype(float)
# Set 'Year by quarter' column as index
gdp_usa_2000.set_index(['Year by quarter'], inplace = True)
#print(gdp_usa_2000[20:40])

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    # Look for the beginning of the recession
    for quarter in range(len(gdp_usa_2000)-2):
        if (gdp_usa_2000.iloc[quarter][0] > gdp_usa_2000.iloc[quarter+1][0]) & (gdp_usa_2000.iloc[quarter+1][0] > gdp_usa_2000.iloc[quarter+2][0]):
            resp02 = gdp_usa_2000.iloc[quarter+1].name
            break
    return resp02
get_recession_start()


# In[42]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    # Look for the recession end
    for quarter in range(len(gdp_usa_2000)-2):
        if (gdp_usa_2000.iloc[quarter][0] > gdp_usa_2000.iloc[quarter+1][0]) & (gdp_usa_2000.iloc[quarter+1][0] > gdp_usa_2000.iloc[quarter+2][0]) & (gdp_usa_2000.iloc[quarter+2][0] < gdp_usa_2000.iloc[quarter+3][0]) & (gdp_usa_2000.iloc[quarter+3][0] < gdp_usa_2000.iloc[quarter+4][0]):
            resp03 = gdp_usa_2000.iloc[quarter+4].name
            break
    return resp03
get_recession_end()


# In[44]:

def get_recession_bottom():
    # Recession period time limit in a new dataframe
    recession = gdp_usa_2000.loc[(gdp_usa_2000.index >= "2008q3") & (gdp_usa_2000.index <= "2009q4")]
    # Take the botton recession quarter
    resp04 = recession.loc[recession['GDP'].idxmin()].name
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    return resp04
get_recession_bottom()


# In[45]:

def add_new_cols():
    #Creating a name list for the new columns
    quarters = ['q1','q2','q3','q4']
    quarters_year = []
    for i in range(2000,2017):
        for x in quarters:
            quarters_year.append((str(i)+x))
    return quarters_year[:67]

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    # Load the 'City_Zhvi_AllHomes.csv' sheet into Panda Dataframe
    data = pd.read_csv('City_Zhvi_AllHomes.csv')
    # New data with columns to 2000q1 until 2016q3
    cols = ['State','RegionName']+[c for c in data.columns[51:252]]
    data = data[cols]
    # Map by dictionary the value of the state abbreviation
    #new_data['State'] = new_data['State'].map(states)
    new_data = data.replace({"State": states})
    # Set 'State' & 'RegionName' columns to be indexs
    new_data.set_index(['State','RegionName'],inplace=True)
    
    #List of quarters to 2000q1 until 2016q3
    quarters = [list(new_data.columns)[x:x+3] for x in range(0, len(list(new_data.columns)), 3)]
    # Names of new columns
    columns_names = add_new_cols()
    
    # Iterating Over two Arrays with zip in parallel
    for column,quarter in zip(columns_names,quarters):
        new_data[column] = new_data[quarter].mean(axis=1)
    
    new_data = new_data[columns_names]
    
    return new_data
convert_housing_data_to_quarters()


# In[47]:

# Copy the results of the recession start (2008q3) and recession end (2009q2)
Rstart = get_recession_start()
Rbotton = get_recession_bottom()

# Obtain a copy of 'City_Zhvi_AllHomes.csv' sheet to 2000q1 until 2016q3
recession = convert_housing_data_to_quarters()
# Obtain the recession period
recession = recession.loc[:,Rstart:Rbotton]
# Reset the index recession dataframe
recession = recession.reset_index()
# Create a new column called 'Difference' between end of recession and the bottom recession
recession['Difference'] = recession['2008q3'] - recession['2009q2']

# Obtain a list of the regions in the universitis
reg_uni_town = get_list_of_university_towns()['RegionName']
# Obtain a list of unique values of universities region
list_uni_town = set(reg_uni_town)

# Create a new column called 'Reg_uni_town' uf a city is part of the list of universities
recession['Reg_uni_town'] = np.where(recession['RegionName'].isin(list_uni_town), 1, 0)

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    # Get a dataframe with the "Difference" values of Reg_uni and Non_Reg_uni
    Reg_uni = recession[recession["Reg_uni_town"] == 1].loc[:,"Difference"].dropna()
    Non_Reg_uni = recession[recession["Reg_uni_town"] == 0].loc[:,"Difference"].dropna()
    
    # Obtain the p value
    p = list(ttest_ind(Non_Reg_uni,Reg_uni))[1]
    
    if p < 0.01:
        different = True
    else:
        different = False
    
    # Obtain the better values on which has a lower mean price ratio 
    if Reg_uni.mean() < Non_Reg_uni.mean():
        better = "university town"
    else:
        better = "non-university town"
        
    return (different,p,better)
run_ttest()


# In[ ]:



