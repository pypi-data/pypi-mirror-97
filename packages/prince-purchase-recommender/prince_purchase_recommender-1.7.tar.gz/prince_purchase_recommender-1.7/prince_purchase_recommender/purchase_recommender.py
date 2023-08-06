#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
import time


# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# # knowing the data

# In[3]:


events_df = pd.read_csv('events.csv')
events_df


# In[4]:


events_df.keys()


# In[5]:


events_df['event'].unique()


# In[6]:


events_df[events_df.transactionid.notnull()].visitorid.unique()    


# visitorid of thoes visitors who made transactions 

# In[7]:


events_df[events_df.transactionid.notnull()].event.unique()


# 'transaction' is recorded in event, whenever transactionid(purchase) is created

# In[8]:


category_df = pd.read_csv('category_tree.csv')


# In[9]:


category_df


# Categoryid explain the relationship of different products with each other, like categoryid 1016 is a child of parentid 213.

# In[10]:


item_properties_1_df = pd.read_csv('item_properties_part1.csv')


# In[11]:


item_properties_1_df


# timestamp is still the same Unix format.
# 
# itemid is the unique item identifier.
# 
# Property is the Item's attributes such as category id and availability while the rest are hashed for confidentiality purposes.
# 
# Value is the item's property value like availability(one of the properties) is 1 if there is stock and 0 otherwise.

# In[12]:


item_properties_1_df.loc[(item_properties_1_df.property == 'categoryid') & (item_properties_1_df.value == '618')].sort_values('timestamp').head()


# above is the number of items under category id 618.

# # Customer Behaviour Exploration
# Its good to categorise coustomers in (a) how made transactions, (b) thoes who do not made transaxtion.

# In[13]:


# all customers who made transaction.
customer_purchased = events_df[events_df.transactionid.notnull()].visitorid.unique()


# In[14]:


len(customer_purchased)


# these many visitors made purchases.
# 
# and their unique 'visitorid' is stored in customer_purchased

# In[15]:


all_customers = events_df.visitorid.unique()


# In[16]:


len(all_customers)
#all the visitors of the item.


# In[17]:


customer_browsed = [x for x in all_customers if x not in customer_purchased]  # this code takes time


# In[18]:


type(customer_browsed),len(customer_browsed)


# In[19]:


customer_browsed = np.isin(all_customers,customer_purchased)  

# another way of doing this.
#customer_browsed = np.array(list(set(all_customers)- set(customer_purchased)))  


# both these codes save time, 


# In[20]:


len(customer_browsed)


# these many customers have visited the item, but did not purchaced it.

# REMEMBER: CUSTOMER_PURCHASED, CUSTOMER_BROWSED, ALL_CUSTOMERS.  ALL CONTAIN UNIQUE 'visitorid', in numpy array

# # Below is a snapshot of visitor id 599528 and their buying journey from viewing to transaction (purchase)

# In[21]:


events_df[events_df.visitorid == 599528].sort_values('timestamp')


# 
# Now, that we know about customer_purchased lets find out which items they purchased.
# 

# In[22]:


purchased_items =[]
for customer in customer_purchased:
    purchased_items.append(list(events_df.loc[(events_df.visitorid == customer) & (events_df.transactionid.notnull())].itemid.unique()))


# purchased_items is a list which contain itemid of purchased items.

# In[23]:


len(purchased_items)


# In[24]:


purchased_items[100:150]


# above data is given in the form of list of lists.
# 
# The inner lists are collection of itemid purchased by single costumer(possibly on different dates).
# 
# This inner list of items can be used to suggest visitors("thoes who buy this also buy following"). Provided the visitor buy any one item from this inner list.

# In[25]:


# As purchase is made 'itemid' is pass through this function along with purchased_items(which is calculated above)
def recommender_bought_bought(item_id, purchased_items):
    recommender_list = []
    for x in purchased_items:        # x(inner_list) is a purchased item
        if item_id in x:             # purchased item is in x(inner_list)
            recommender_list += x
    recommender_list = list(set(recommender_list) - set([item_id]))
    
    return recommender_list


# In[26]:


# Check: recommender_bought_bought()
recommender_bought_bought(302422, purchased_items)


# So now we can present to the visitor a list of the other items a customer previously bought along with what item the current visitor is viewing e.g. item number 302422

# In[37]:


recommender_bought_bought(217218, purchased_items)    # itemid = '217218'


# In[42]:


recommender_bought_bought(428040, purchased_items)     # itemid = '428040'


# In[44]:


recommender_bought_bought(321984, purchased_items)     # itemid = '321984'


# In[47]:


recommender_bought_bought(291964, purchased_items)     # itemid = '291964'


# In[50]:


recommender_bought_bought(85771, purchased_items)     # itemid = '85771'


# 
