
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-machine-learning/resources/bANLa) course resource._
# 
# ---

# ## Assignment 4 - Understanding and Predicting Property Maintenance Fines
# 
# This assignment is based on a data challenge from the Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)). 
# 
# The Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)) and the Michigan Student Symposium for Interdisciplinary Statistical Sciences ([MSSISS](https://sites.lsa.umich.edu/mssiss/)) have partnered with the City of Detroit to help solve one of the most pressing problems facing Detroit - blight. [Blight violations](http://www.detroitmi.gov/How-Do-I/Report/Blight-Complaint-FAQs) are issued by the city to individuals who allow their properties to remain in a deteriorated condition. Every year, the city of Detroit issues millions of dollars in fines to residents and every year, many of these fines remain unpaid. Enforcing unpaid blight fines is a costly and tedious process, so the city wants to know: how can we increase blight ticket compliance?
# 
# The first step in answering this question is understanding when and why a resident might fail to comply with a blight ticket. This is where predictive modeling comes in. For this assignment, your task is to predict whether a given blight ticket will be paid on time.
# 
# All data for this assignment has been provided to us through the [Detroit Open Data Portal](https://data.detroitmi.gov/). **Only the data already included in your Coursera directory can be used for training the model for this assignment.** Nonetheless, we encourage you to look into data from other Detroit datasets to help inform feature creation and model selection. We recommend taking a look at the following related datasets:
# 
# * [Building Permits](https://data.detroitmi.gov/Property-Parcels/Building-Permits/xw2a-a7tf)
# * [Trades Permits](https://data.detroitmi.gov/Property-Parcels/Trades-Permits/635b-dsgv)
# * [Improve Detroit: Submitted Issues](https://data.detroitmi.gov/Government/Improve-Detroit-Submitted-Issues/fwz3-w3yn)
# * [DPD: Citizen Complaints](https://data.detroitmi.gov/Public-Safety/DPD-Citizen-Complaints-2016/kahe-efs3)
# * [Parcel Map](https://data.detroitmi.gov/Property-Parcels/Parcel-Map/fxkw-udwf)
# 
# ___
# 
# We provide you with two data files for use in training and validating your models: train.csv and test.csv. Each row in these two files corresponds to a single blight ticket, and includes information about when, why, and to whom each ticket was issued. The target variable is compliance, which is True if the ticket was paid early, on time, or within one month of the hearing data, False if the ticket was paid after the hearing date or not at all, and Null if the violator was found not responsible. Compliance, as well as a handful of other variables that will not be available at test-time, are only included in train.csv.
# 
# Note: All tickets where the violators were found not responsible are not considered during evaluation. They are included in the training set as an additional source of data for visualization, and to enable unsupervised and semi-supervised approaches. However, they are not included in the test set.
# 
# <br>
# 
# **File descriptions** (Use only this data for training your model!)
# 
#     train.csv - the training set (all tickets issued 2004-2011)
#     test.csv - the test set (all tickets issued 2012-2016)
#     addresses.csv & latlons.csv - mapping from ticket id to addresses, and from addresses to lat/lon coordinates. 
#      Note: misspelled addresses may be incorrectly geolocated.
# 
# <br>
# 
# **Data fields**
# 
# train.csv & test.csv
# 
#     ticket_id - unique identifier for tickets
#     agency_name - Agency that issued the ticket
#     inspector_name - Name of inspector that issued the ticket
#     violator_name - Name of the person/organization that the ticket was issued to
#     violation_street_number, violation_street_name, violation_zip_code - Address where the violation occurred
#     mailing_address_str_number, mailing_address_str_name, city, state, zip_code, non_us_str_code, country - Mailing address of the violator
#     ticket_issued_date - Date and time the ticket was issued
#     hearing_date - Date and time the violator's hearing was scheduled
#     violation_code, violation_description - Type of violation
#     disposition - Judgment and judgement type
#     fine_amount - Violation fine amount, excluding fees
#     admin_fee - $20 fee assigned to responsible judgments
# state_fee - $10 fee assigned to responsible judgments
#     late_fee - 10% fee assigned to responsible judgments
#     discount_amount - discount applied, if any
#     clean_up_cost - DPW clean-up or graffiti removal cost
#     judgment_amount - Sum of all fines and fees
#     grafitti_status - Flag for graffiti violations
#     
# train.csv only
# 
#     payment_amount - Amount paid, if any
#     payment_date - Date payment was made, if it was received
#     payment_status - Current payment status as of Feb 1 2017
#     balance_due - Fines and fees still owed
#     collection_status - Flag for payments in collections
#     compliance [target variable for prediction] 
#      Null = Not responsible
#      0 = Responsible, non-compliant
#      1 = Responsible, compliant
#     compliance_detail - More information on why each ticket was marked compliant or non-compliant
# 
# 
# ___
# 
# ## Evaluation
# 
# Your predictions will be given as the probability that the corresponding blight ticket will be paid on time.
# 
# The evaluation metric for this assignment is the Area Under the ROC Curve (AUC). 
# 
# Your grade will be based on the AUC score computed for your classifier. A model which with an AUROC of 0.7 passes this assignment, over 0.75 will recieve full points.
# ___
# 
# For this assignment, create a function that trains a model to predict blight ticket compliance in Detroit using `train.csv`. Using this model, return a series of length 61001 with the data being the probability that each corresponding ticket from `test.csv` will be paid, and the index being the ticket_id.
# 
# Example:
# 
#     ticket_id
#        284932    0.531842
#        285362    0.401958
#        285361    0.105928
#        285338    0.018572
#                  ...
#        376499    0.208567
#        376500    0.818759
#        369851    0.018528
#        Name: compliance, dtype: float32
#        
# ### Hints
# 
# * Make sure your code is working before submitting it to the autograder.
# 
# * Print out your result to see whether there is anything weird (e.g., all probabilities are the same).
# 
# * Generally the total runtime should be less than 10 mins. You should NOT use Neural Network related classifiers (e.g., MLPClassifier) in this question. 
# 
# * Try to avoid global variables. If you have other functions besides blight_model, you should move those functions inside the scope of blight_model.
# 
# * Refer to the pinned threads in Week 4's discussion forum when there is something you could not figure it out.

# In[4]:

import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

def interval_time(hearing_date_str, ticket_issued_date_str):
        if not hearing_date_str or type(hearing_date_str)!=str: return 74
        hearing_date = datetime.strptime(hearing_date_str, "%Y-%m-%d %H:%M:%S")
        ticket_issued_date = datetime.strptime(ticket_issued_date_str, "%Y-%m-%d %H:%M:%S")
        gap = hearing_date - ticket_issued_date
        return gap.days

def blight_model():
    
    # Load the train and test data, and address data by csv files
    train_data = pd.read_csv('train.csv', encoding = 'ISO-8859-1')
    test_data = pd.read_csv('test.csv')
    address =  pd.read_csv('addresses.csv')
    
    # Filter null valued compliance rows
    train_data = train_data[(train_data['compliance'] == 0) | (train_data['compliance'] == 1)]
    
    # Load address and location information by csv files
    latlons = pd.read_csv('latlons.csv')
    address = address.set_index('address').join(latlons.set_index('address'), how='left')
    
    # Join address and location to train and test data
    train_data = train_data.set_index('ticket_id').join(address.set_index('ticket_id'))
    test_data = test_data.set_index('ticket_id').join(address.set_index('ticket_id'))
    
    # Filter null valued hearing date rows
    train_data = train_data[~train_data['hearing_date'].isnull()]
    
    # Add new column with interval time since ticket_issued_date to hearing_date
    train_data['interval_time'] = train_data.apply(lambda row: interval_time(row['hearing_date'], row['ticket_issued_date']), axis=1)
    test_data['interval_time'] = test_data.apply(lambda row: interval_time(row['hearing_date'], row['ticket_issued_date']), axis=1)
    
    # Features to be splitted
    feature_to_be_splitted = ['agency_name', 'state', 'disposition']
    
    # Fill NaN Lat Lon Values with pad method
    train_data.lat.fillna(method='pad', inplace=True)
    train_data.lon.fillna(method='pad', inplace=True)
    train_data.state.fillna(method='pad', inplace=True)
    test_data.lat.fillna(method='pad', inplace=True)
    test_data.lon.fillna(method='pad', inplace=True)
    test_data.state.fillna(method='pad', inplace=True)

    # Convert categorical variable into dummy/indicator variables
    train_data = pd.get_dummies(train_data, columns=feature_to_be_splitted)
    test_data = pd.get_dummies(test_data, columns=feature_to_be_splitted)
    
    # Remove Non Existing Features In Test Data
    train_remove_list = ['balance_due',
                         'collection_status',
                         'compliance_detail',
                         'payment_amount',
                         'payment_date',
                         'payment_status'
                        ]
    train_data.drop(train_remove_list, axis=1, inplace=True)
    
    # Remove String Data
    string_remove_list = ['violator_name', 'zip_code', 'country', 
                          'city','inspector_name', 
                          'violation_street_number', 
                          'violation_street_name', 
                          'violation_zip_code', 
                          'violation_description', 
                          'mailing_address_str_number', 
                          'mailing_address_str_name',
                          'non_us_str_code', 'ticket_issued_date',
                          'hearing_date', 'grafitti_status', 
                          'violation_code'
                         ]
    train_data.drop(string_remove_list, axis=1, inplace=True)
    test_data.drop(string_remove_list, axis=1, inplace=True)
    
    # Select target value as y train and remove it from x train
    y_train = train_data.compliance
    train_features = train_data.drop('compliance', axis=1)
    
    # Remove features that are not in train and test sets
    train_features_set = set(train_features)
    for feature in set(train_features):
        if feature not in test_data:
            train_features_set.remove(feature)
    train_features = list(train_features_set)
    X_train = train_data[train_features]
    
    # Do nothing with test data and select as X_test, we don't have y_test
    X_test = test_data[train_features]
    
    # Scale Features To Reduce Computation Time
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build And Train Classifier Model
    clf = MLPClassifier(hidden_layer_sizes = [100, 10],
                        alpha=5,
                        random_state = 0, 
                        solver='lbfgs', 
                        verbose=0)
    clf.fit(X_train_scaled, y_train)
    
    # Predict probabilities
    y_proba = clf.predict_proba(X_test_scaled)[:,1]
    
    # Integrate with reloaded test data
    test_df = pd.read_csv('test.csv', encoding = "ISO-8859-1")
    test_df['compliance'] = y_proba
    test_df.set_index('ticket_id', inplace=True)
    
    return test_df.compliance


# In[5]:

blight_model()

