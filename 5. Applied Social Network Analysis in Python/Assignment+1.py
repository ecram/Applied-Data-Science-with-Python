
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-social-network-analysis/resources/yPcBs) course resource._
# 
# ---

# # Assignment 1 - Creating and Manipulating Graphs
# 
# Eight employees at a small company were asked to choose 3 movies that they would most enjoy watching for the upcoming company movie night. These choices are stored in the file `Employee_Movie_Choices.txt`.
# 
# A second file, `Employee_Relationships.txt`, has data on the relationships between different coworkers. 
# 
# The relationship score has value of `-100` (Enemies) to `+100` (Best Friends). A value of zero means the two employees haven't interacted or are indifferent.
# 
# Both files are tab delimited.

# In[1]:

import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite


# This is the set of employees
employees = set(['Pablo',
                 'Lee',
                 'Georgia',
                 'Vincent',
                 'Andy',
                 'Frida',
                 'Joan',
                 'Claude'])

# This is the set of movies
movies = set(['The Shawshank Redemption',
              'Forrest Gump',
              'The Matrix',
              'Anaconda',
              'The Social Network',
              'The Godfather',
              'Monty Python and the Holy Grail',
              'Snakes on a Plane',
              'Kung Fu Panda',
              'The Dark Knight',
              'Mean Girls'])


# you can use the following function to plot graphs
# make sure to comment it out before submitting to the autograder
def plot_graph(G, weight_name=None):
    '''
    G: a networkx G
    weight_name: name of the attribute for plotting edge weights (if G is weighted)
    '''
    get_ipython().magic('matplotlib notebook')
    import matplotlib.pyplot as plt
    
    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    weights = None
    
    if weight_name:
        weights = [int(G[u][v][weight_name]) for u,v in edges]
        labels = nx.get_edge_attributes(G,weight_name)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        nx.draw_networkx(G, pos, edges=edges, width=weights);
    else:
        nx.draw_networkx(G, pos, edges=edges);


# ### Question 1
# 
# Using NetworkX, load in the bipartite graph from `Employee_Movie_Choices.txt` and return that graph.
# 
# *This function should return a networkx graph with 19 nodes and 24 edges*

# In[2]:

def answer_one():    
    G = nx.read_edgelist('Employee_Movie_Choices.txt', delimiter="\t")
    return G
answer_one()


# In[3]:

aux = answer_one().edges(data=True)
B = nx.Graph()
B.add_nodes_from(list(employees), bipartite=0)
B.add_nodes_from(list(movies), bipartite=1)
B.add_edges_from(aux)


# In[16]:

'''
%matplotlib notebook
import matplotlib.pyplot as plt
plt.figure()

edges = B.edges()
print(edges)
X, Y = bipartite.sets(B)
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
nx.draw_networkx(B, pos=pos, edges=edges)
plt.show()
plt.savefig('movies_choise.png')
'''


# ### Question 2
# 
# Using the graph from the previous question, add nodes attributes named `'type'` where movies have the value `'movie'` and employees have the value `'employee'` and return that graph.
# 
# *This function should return a networkx graph with node attributes `{'type': 'movie'}` or `{'type': 'employee'}`*

# In[19]:

def answer_two():
    
    B = answer_one()
    for node in B.nodes():
        if node in employees:
            B.add_node(node, type="employee")
        else:
            B.add_node(node, type="movie")
    
    return B


# ### Question 3
# 
# Find a weighted projection of the graph from `answer_two` which tells us how many movies different pairs of employees have in common.
# 
# *This function should return a weighted projected graph.*

# In[21]:

def answer_three():
    aux = answer_one().edges(data=True)
    B = nx.Graph()
    B.add_nodes_from(list(employees), bipartite=0)
    B.add_nodes_from(list(movies), bipartite=1)
    B.add_edges_from(aux)
    P = bipartite.weighted_projected_graph(B,employees)
    
    return P

#answer_three().edges(data=True)


# ### Question 4
# 
# Suppose you'd like to find out if people that have a high relationship score also like the same types of movies.
# 
# Find the Pearson correlation ( using `DataFrame.corr()` ) between employee relationship scores and the number of movies they have in common. If two employees have no movies in common it should be treated as a 0, not a missing value, and should be included in the correlation calculation.
# 
# *This function should return a float.*

# In[63]:

def answer_four():  
    G_df_ERE = pd.read_csv("Employee_Relationships.txt", delimiter="\t", header=None, 
                           names=['employee_a', 'employee_b', 'relationship_score'])
    G_df_EMC = answer_three()
    G_df_EMC = pd.DataFrame(G_df_EMC.edges(data=True), columns=['employee_a', 'employee_b', 'movie_score'])
    G_df_EMC_copy = G_df_EMC[["employee_b", "employee_a", "movie_score"]].copy()
    G_df_EMC_copy.rename(columns={"employee_b":"employee_a", "employee_a":"employee_b"}, inplace=True)
    G_df_EMC = pd.concat([G_df_EMC, G_df_EMC_copy])
    final_df = pd.merge(G_df_EMC, G_df_ERE, on = ['employee_a', 'employee_b'], how='right')
    final_df['movies_score'] = final_df['movie_score'].map(lambda x: x['weight'] if type(x)==dict else None)
    final_df['movies_score'].fillna(value=0, inplace=True)
    return final_df['movies_score'].corr(final_df['relationship_score'])
    
answer_four()

