
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 2 - Introduction to NLTK
# 
# In part 1 of this assignment you will use nltk to explore the Herman Melville novel Moby Dick. Then in part 2 you will create a spelling recommender function that uses nltk to find words similar to the misspelling. 

# ## Part 1 - Analyzing Moby Dick

# In[1]:

import nltk
import pandas as pd
import numpy as np

# If you would like to work with the raw text you can use 'moby_raw'
with open('moby.txt', 'r') as f:
    moby_raw = f.read()
    
# If you would like to work with the novel in nltk.Text format you can use 'text1'
moby_tokens = nltk.word_tokenize(moby_raw)
text1 = nltk.Text(moby_tokens)


# ### Example 1
# 
# How many tokens (words and punctuation symbols) are in text1?
# 
# *This function should return an integer.*

# In[2]:

def example_one():
    
    return len(nltk.word_tokenize(moby_raw)) # or alternatively len(text1)

example_one()


# ### Example 2
# 
# How many unique tokens (unique words and punctuation) does text1 have?
# 
# *This function should return an integer.*

# In[3]:

def example_two():
    
    return len(set(nltk.word_tokenize(moby_raw))) # or alternatively len(set(text1))

example_two()


# ### Example 3
# 
# After lemmatizing the verbs, how many unique tokens does text1 have?
# 
# *This function should return an integer.*

# In[4]:

from nltk.stem import WordNetLemmatizer

def example_three():

    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(w,'v') for w in text1]

    return len(set(lemmatized))

example_three()


# In[5]:

from nltk import FreqDist
dist = FreqDist(moby_tokens)
text1[:10]


# ### Question 1
# 
# What is the lexical diversity of the given text input? (i.e. ratio of unique tokens to the total number of tokens)
# 
# *This function should return a float.*

# In[6]:

def answer_one():
    
    return len(set(nltk.word_tokenize(moby_raw)))/len(nltk.word_tokenize(moby_raw))

answer_one()


# ### Question 2
# 
# What percentage of tokens is 'whale'or 'Whale'?
# 
# *This function should return a float.*

# In[7]:

from nltk import FreqDist
#fdist = FreqDist([w.lower() for w in news_text])
def answer_two():
    dist = FreqDist(moby_tokens)
    #print(len(moby_tokens))
    #print(dist)
    #print(len(dist.values()))
    #print(dist.values())
    return (dist['whale']+dist['Whale'])/sum(dist.values())*100

answer_two()


# ### Question 3
# 
# What are the 20 most frequently occurring (unique) tokens in the text? What is their frequency?
# 
# *This function should return a list of 20 tuples where each tuple is of the form `(token, frequency)`. The list should be sorted in descending order of frequency.*

# In[8]:

def answer_three():
    dist = FreqDist(moby_tokens)
    return sorted(dist.items(), key=lambda x:x[1], reverse = True)[:20]

answer_three()


# ### Question 4
# 
# What tokens have a length of greater than 5 and frequency of more than 150?
# 
# *This function should return a sorted list of the tokens that match the above constraints. To sort your list, use `sorted()`*

# In[9]:

def answer_four():
    #vocab1 = dist.keys()
    #freqwords = [w for w in vocab1 if len(w) > 5 and dist[w] > 150]
    #freqwords.sort()
    #print(freqwords)
    FreqTokens = [token for token in set(moby_tokens) if len(token) > 5 and dist[token] > 150]
    FreqTokens.sort()
    return FreqTokens

answer_four()


# ### Question 5
# 
# Find the longest word in text1 and that word's length.
# 
# *This function should return a tuple `(longest_word, length)`.*

# In[10]:

print(text1[:20])
print(type(text1))
#print(moby_raw)


# In[11]:

def answer_five():
    longest_word = ''
    for word in text1:
        if len(word) > len(longest_word):
            longest_word = word
    print(longest_word)
    return longest_word, len(longest_word)

answer_five()


# ### Question 6
# 
# What unique words have a frequency of more than 2000? What is their frequency?
# 
# "Hint:  you may want to use `isalpha()` to check if the token is a word and not punctuation."
# 
# *This function should return a list of tuples of the form `(frequency, word)` sorted in descending order of frequency.*

# In[12]:

def answer_six():
    vocab1 = dist.keys()
    freqwords = [w for w in vocab1 if w.isalpha() and dist[w] > 2000]
    MostFreq = []
    for fw in freqwords:
        MostFreq.append(tuple((dist[fw],fw)))
    
    MostFreq.sort(key=lambda tup: tup[0], reverse = True)
    
    return MostFreq

answer_six()


# ### Question 7
# 
# What is the average number of tokens per sentence?
# 
# *This function should return a float.*

# In[13]:

def answer_seven():
    sentences = nltk.sent_tokenize(moby_raw)
    
    return len(moby_tokens)/len(sentences)

answer_seven()


# ### Question 8
# 
# What are the 5 most frequent parts of speech in this text? What is their frequency?
# 
# *This function should return a list of tuples of the form `(part_of_speech, frequency)` sorted in descending order of frequency.*

# In[26]:

from collections import Counter
def answer_eight():
    counter = Counter()
    tagged_tokens = nltk.pos_tag(moby_tokens)
    for t in tagged_tokens:
        counter[t[1]] += 1
    return counter.most_common(5)

answer_eight()


# ## Part 2 - Spelling Recommender
# 
# For this part of the assignment you will create three different spelling recommenders, that each take a list of misspelled words and recommends a correctly spelled word for every word in the list.
# 
# For every misspelled word, the recommender should find find the word in `correct_spellings` that has the shortest distance*, and starts with the same letter as the misspelled word, and return that word as a recommendation.
# 
# *Each of the three different recommenders will use a different distance measure (outlined below).
# 
# Each of the recommenders should provide recommendations for the three default words provided: `['cormulent', 'incendenece', 'validrate']`.

# In[32]:

from nltk.corpus import words

correct_spellings = words.words()


# ### Question 9
# 
# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
# 
# **[Jaccard distance](https://en.wikipedia.org/wiki/Jaccard_index) on the trigrams of the two words.**
# 
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*

# In[41]:

def answer_nine(entries=['cormulent', 'incendenece', 'validrate']):
    answer = []
    correct_spellings2 = [w for w in correct_spellings if len(w) > 3]
    for entry in entries:
        options = [w for w in correct_spellings2 if w[0] == entry[0] and w[1] == entry[1] and w[2] == entry[2]]
        answer.append(min(options, key = lambda option:nltk.jaccard_distance(set(nltk.ngrams(entry, n=3)), 
                                                                              set(nltk.ngrams(option, n=3)))))
    
    return answer
    
answer_nine()


# ### Question 10
# 
# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
# 
# **[Jaccard distance](https://en.wikipedia.org/wiki/Jaccard_index) on the 4-grams of the two words.**
# 
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*

# In[43]:

def answer_ten(entries=['cormulent', 'incendenece', 'validrate']):
    answer = []
    correct_spellings2 = [w for w in correct_spellings if len(w) > 3]
    for entry in entries:
        options = [w for w in correct_spellings2 if w[0] == entry[0] and w[1] == entry[1] and w[2] == entry[2]]
        answer.append(min(options, key = lambda option:nltk.jaccard_distance(set(nltk.ngrams(entry, n=4)), 
                                                                              set(nltk.ngrams(option, n=4)))))
    
    return answer
    
answer_ten()


# ### Question 11
# 
# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
# 
# **[Edit distance on the two words with transpositions.](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance)**
# 
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*

# In[42]:

def answer_eleven(entries=['cormulent', 'incendenece', 'validrate']):
    answer = []
    correct_spellings2 = [w for w in correct_spellings if len(w) > 3]
    for entry in entries:
        options = [w for w in correct_spellings2 if w[0] == entry[0] and w[1] == entry[1] and w[2] == entry[2]]
        answer.append(min(options, key = lambda option:nltk.edit_distance(entry,option)))
    
    return answer
    
answer_eleven()


# In[ ]:



