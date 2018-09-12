
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# * Watch out for potential typos as this is a raw, real-life derived dataset.
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[1]:

import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
#df.to_csv('dates.csv', encoding='utf-8')


# In[2]:

import numpy as np

def date_sorter():
    # List of formats:
    # 1) dd/mm/aaaa or d/m/aa or dd-mm-aaaa or d-m-aa
    one_list = df.str.extract(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})')
    # 2) {d}d -|,|.|_ MMM* -|,|.|_ {yy}yy
    two_list = df.str.extract(r'(\d{1,2}(?:-|\.|,|\s)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\.|\s)\d{2,4})')
    # 3) MMM* -|,|.|_ {d}d th|st|nd-|,|.|_ {aa}aa
    thr_list = df.str.extract(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\.)?\s\d{1,2}(?:,|\.|-|th|st|nd)?\s\d{2,4})')
    #aux_list = df.str.extract(r'((?:\d{1,2})?(?:-|\s|\.|,|.)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\s|\.)\s?\d{1,2}?(?:th|st|nd|-|,|\s|\.)?\s?\d{2,4})')

    # 4) 
    #Feb 2009; Sep 2009; Oct 2010
    #four1_list = df.str.extract(r'([^0-9]\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\.)?\s\d{4})')
    four2_list = df.str.extract(r'([^0-9]\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\.)?\s\d{4})')
    fou_list = four2_list.str.extract(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\.)?\s\d{4})')
    #fou_list = pd.concat([four1_list,four2_list])
    #four_list = df.str.extract(r'((?:\d{,2}\s)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|\.|\s|,)\s?\d{,2}[a-z]*(?:-|,|\s)?\s?\d{2,4})')

    # 5) (|a-z|A-z".Feb 2009
    five_list = df.str.extract(r'((?:\)|\(|\w|"|^|\.)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\.)?\s\d{4})')
    fiv_list = five_list.str.extract(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:-|,|\.)?\s\d{4})')

    # 6) ^6/2008; 12/2009
    sixs_list = df.str.extract(r'((?:^)\d{1,2}[\/]\d{4})')
    six_list = sixs_list.str.extract(r'(\d{1,2}[\/]\d{4})')

    # 7) 6/2008; 12/2009
    seven_list = df.str.extract(r'((?:\s|~|\)|\(|n|-|e)\d{1,2}[\/]\d{4})')
    sev_list = seven_list.str.extract(r'(\d{1,2}[\/]\d{4})')

    # 8) 2009; 2010
    eight_list = df.str.extract(r'((?:\w|\(|\)|\s|\.|~)\d{4})')
    eig_list = eight_list.str.extract(r'(\d{4})')

    # 9) ^2009; 2010
    nine_list = df.str.extract(r'((?:^)\d{4})')
    nin_list = nine_list.str.extract(r'(\d{4})')

    one = one_list
    two = two_list
    three = thr_list
    four = fou_list
    five = fiv_list
    six = six_list
    seven = sev_list
    eight = eig_list
    nine = nin_list
    dates = pd.to_datetime(one.fillna(two).fillna(three).fillna(four).fillna(five).fillna(six).fillna(seven).fillna(eight).fillna(nine).replace('Decemeber','December',regex=True).replace('Janaury','January',regex=True))
    dates.to_csv('dates2', sep='\t', encoding='utf-8')
    myList = pd.Series(dates.sort_values())
    answer = pd.Series([i[0] for i in sorted(enumerate(dates), key=lambda x:x[1])],np.arange(500))
    return answer


# In[3]:

date_sorter()


# In[ ]:



