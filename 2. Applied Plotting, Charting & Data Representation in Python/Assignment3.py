
# coding: utf-8

# # Assignment 3 - Building a Custom Visualization
# 
# ---
# 
# In this assignment you must choose one of the options presented below and submit a visual as well as your source code for peer grading. The details of how you solve the assignment are up to you, although your assignment must use matplotlib so that your peers can evaluate your work. The options differ in challenge level, but there are no grades associated with the challenge level you chose. However, your peers will be asked to ensure you at least met a minimum quality for a given technique in order to pass. Implement the technique fully (or exceed it!) and you should be able to earn full grades for the assignment.
# 
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ferreira, N., Fisher, D., & Konig, A. C. (2014, April). [Sample-oriented task-driven visualizations: allowing users to make better, more confident decisions.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 571-580). ACM. ([video](https://www.youtube.com/watch?v=BI7GAs-va-Q))
# 
# 
# In this [paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) the authors describe the challenges users face when trying to make judgements about probabilistic data generated through samples. As an example, they look at a bar chart of four years of data (replicated below in Figure 1). Each year has a y-axis value, which is derived from a sample of a larger dataset. For instance, the first value might be the number votes in a given district or riding for 1992, with the average being around 33,000. On top of this is plotted the 95% confidence interval for the mean (see the boxplot lectures for more information, and the yerr parameter of barcharts).
# 
# <br>
# <img src="readonly/Assignment3Fig1.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1 from (Ferreira et al, 2014).</h4>
# 
# <br>
# 
# A challenge that users face is that, for a given y-axis value (e.g. 42,000), it is difficult to know which x-axis values are most likely to be representative, because the confidence levels overlap and their distributions are different (the lengths of the confidence interval bars are unequal). One of the solutions the authors propose for this problem (Figure 2c) is to allow users to indicate the y-axis value of interest (e.g. 42,000) and then draw a horizontal line and color bars based on this value. So bars might be colored red if they are definitely above this value (given the confidence interval), blue if they are definitely below this value, or white if they contain this value.
# 
# 
# <br>
# <img src="readonly/Assignment3Fig2c.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  Figure 2c from (Ferreira et al. 2014). Note that the colorbar legend at the bottom as well as the arrows are not required in the assignment descriptions below.</h4>
# 
# <br>
# <br>
# 
# **Easiest option:** Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.
# 
# 
# **Harder option:** Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).
# 
# **Even Harder option:** Add interactivity to the above, which allows the user to click on the y axis to set the value of interest. The bar colors should change with respect to what value the user has selected.
# 
# **Hardest option:** Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).
# 
# ---
# 
# *Note: The data given for this assignment is not the same as the data used in the article and as a result the visualizations may look a little different.*

# In[27]:

# Use the following data for this assignment:

import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df


# In[28]:

# Import necessary libriries
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib notebook')
from scipy import stats
import matplotlib.colors as mcol
import matplotlib.cm as cm


# In[29]:

# 1. Calculate the mean (m) for year in df
## year_avg ==> m
m = df.mean(axis = 1)

# Calculate the standard deviation
## year_std ==> ci
ci = df.std(axis = 1)

# Calculate the margin of error (yerr): where margin of error = standard error* C 
# (C is a constant determined by the 95% (Critical value or T-value of 95% of a normal distribution) 
# i.e.abs(qnorm( (1-.95)/2 percentile)), for a normal distribution C is approximately 1.96
yerr = ci / np.sqrt(df.shape[1]) * stats.t.ppf(1-0.05/2, df.shape[1]-1)


# In[30]:

# 2. plot a bar chart using m and ci, the chart should look like the Figure 1 from (Ferreira et al, 2014) 
# shown in the assignment description

plt.figure()
bars = plt.bar(range(df.shape[0]), m, yerr = yerr, capsize=11, align='center', color = 'dodgerblue')


# In[31]:

# 3. plot a horizontal line Y

fig = plt.gcf()
threshold = 40000
#plt.axhline(y = threshold, color = 'k', alpha = 0.5)
plt.axhline(y=y_test, color='k', alpha=0.5, label='Y= {}'.format(y_test))


# In[32]:

# 4. based on the value of y (this can be inputed through the update function of the animation or manually)
# set the colour of each of the columns in the bar chart, this can be done using an if or switch statement
cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["darkblue", "lightskyblue", "dodgerblue"])
cpick = cm.ScalarMappable(cmap=cm1)
cpick.set_array([])

percentages = []

for bar, yerr_ in zip(bars, yerr):
    low = bar.get_height() - yerr_
    high = bar.get_height() + yerr_
    percentage = (high-threshold)/(high-low)
    if percentage>1: percentage = 1
    if percentage<0: percentage=0
    percentages.append(percentage)
    
cpick.to_rgba(percentages)

plt.xticks(range(df.shape[0]), df.index, alpha = 0.7)
bars = plt.bar(range(df.shape[0]), m, yerr = yerr, color = cpick.to_rgba(percentages))
plt.colorbar(cpick, orientation='horizontal')
plt.ylabel('Number of Votes and 95% CI')
plt.legend()


# In[ ]:



