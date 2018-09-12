
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-social-network-analysis/resources/yPcBs) course resource._
# 
# ---

# # Assignment 2 - Network Connectivity
# 
# In this assignment you will go through the process of importing and analyzing an internal email communication network between employees of a mid-sized manufacturing company. 
# Each node represents an employee and each directed edge between two nodes represents an individual email. The left node represents the sender and the right node represents the recipient.

# In[2]:

import networkx as nx

# This line must be commented out when submitting to the autograder
#!head email_network.txt


# ### Question 1
# 
# Using networkx, load up the directed multigraph from `email_network.txt`. Make sure the node names are strings.
# 
# *This function should return a directed multigraph networkx graph.*

# In[10]:

def answer_one():
    G = nx.read_edgelist("email_network.txt", delimiter='\t', data=[('timestamp', int)], create_using=nx.MultiDiGraph())
    return G
G = answer_one()


# ### Question 2
# 
# How many employees and emails are represented in the graph from Question 1?
# 
# *This function should return a tuple (#employees, #emails).*

# In[11]:

def answer_two():
    return len(G.nodes()), len(G.edges())
#answer_two()


# ### Question 3
# 
# * Part 1. Assume that information in this company can only be exchanged through email.
# 
#     When an employee sends an email to another employee, a communication channel has been created, allowing the sender to provide information to the receiver, but not vice versa. 
# 
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
# 
# 
# * Part 2. Now assume that a communication channel established by an email allows information to be exchanged both ways. 
# 
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
# 
# 
# *This function should return a tuple of bools (part1, part2).*

# In[12]:

def answer_three():
    return (nx.is_strongly_connected(G),nx.is_connected(G.to_undirected()))
#answer_three()


# ### Question 4
# 
# How many nodes are in the largest (in terms of nodes) weakly connected component?
# 
# *This function should return an int.*

# In[17]:

def answer_four():
    aux = sorted(nx.weakly_connected_components(G))
    return len(max(aux, key=len))
#answer_four()


# ### Question 5
# 
# How many nodes are in the largest (in terms of nodes) strongly connected component?
# 
# *This function should return an int*

# In[15]:

def answer_five():
    aux = sorted(nx.strongly_connected_components(G))
    return len(max(aux, key=len))
#answer_five()


# ### Question 6
# 
# Using the NetworkX function strongly_connected_component_subgraphs, find the subgraph of nodes in a largest strongly connected component. 
# Call this graph G_sc.
# 
# *This function should return a networkx MultiDiGraph named G_sc.*

# In[26]:

def answer_six():
    aux = nx.strongly_connected_component_subgraphs(G)
    return max(aux, key=len)
G_sc = answer_six()


# ### Question 7
# 
# What is the average distance between nodes in G_sc?
# 
# *This function should return a float.*

# In[27]:

def answer_seven():    
    return nx.average_shortest_path_length(G_sc)
#answer_seven()


# ### Question 8
# 
# What is the largest possible distance between two employees in G_sc?
# 
# *This function should return an int.*

# In[29]:

def answer_eight():
    return nx.diameter(G_sc)
#answer_eight()


# ### Question 9
# 
# What is the set of nodes in G_sc with eccentricity equal to the diameter?
# 
# *This function should return a set of the node(s).*

# In[43]:

def answer_nine():
    return set(nx.periphery(G_sc))
#answer_nine()


# ### Question 10
# 
# What is the set of node(s) in G_sc with eccentricity equal to the radius?
# 
# *This function should return a set of the node(s).*

# In[44]:

def answer_ten():
    return set(nx.center(G_sc))
#answer_ten()


# ### Question 11
# 
# Which node in G_sc is connected to the most other nodes by a shortest path of length equal to the diameter of G_sc?
# 
# How many nodes are connected to this node?
# 
# 
# *This function should return a tuple (name of node, number of satisfied connected nodes).*

# In[36]:

def answer_eleven():
    G_sc_diameter = answer_eight()
    G_sc_periphery = answer_nine()
    max_count_nodes = -1
    the_node = None
    for node in G_sc_periphery:
        shortest_path_to_node = nx.shortest_path_length(G_sc, node)
        count_diameter_node = list(shortest_path_to_node.values()).count(G_sc_diameter)
        if count_diameter_node > max_count_nodes:
            the_node = node
            max_count_nodes = count_diameter_node
    return (the_node, max_count_nodes)
#answer_eleven()


# ### Question 12
# 
# Suppose you want to prevent communication from flowing to the node that you found in the previous question from any node in the center of G_sc, what is the smallest number of nodes you would need to remove from the graph (you're not allowed to remove the node from the previous question or the center nodes)? 
# 
# *This function should return an integer.*

# In[37]:

def answer_twelve():
    node = answer_eleven()[0]
    center = nx.center(G_sc)[0]
    return len(nx.minimum_node_cut(G_sc, center, node))
#answer_twelve()


# ### Question 13
# 
# Construct an undirected graph G_un using G_sc (you can ignore the attributes).
# 
# *This function should return a networkx Graph.*

# In[41]:

def answer_thirteen():
    G_und_graph = G_sc.to_directed()
    return nx.Graph(G_und_graph)
#answer_thirteen()


# ### Question 14
# 
# What is the transitivity and average clustering coefficient of graph G_un?
# 
# *This function should return a tuple (transitivity, avg clustering).*

# In[42]:

def answer_fourteen():
    G_und_graph = answer_thirteen()
    return (nx.transitivity(G_und_graph), nx.average_clustering(G_und_graph))
#answer_fourteen()

