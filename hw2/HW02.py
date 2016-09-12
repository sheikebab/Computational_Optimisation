
# coding: utf-8

# In[1]:

import pandas as pd


# In[2]:

df = pd.read_csv('NMC_v4_0.csv')


# In[7]:

# df


# In[12]:

def get_cinc(df, country_code, year):
    cinc_value = df[(df.ccode == country_code) & (df.year == year)].cinc
    return cinc_value


# In[13]:

print (get_cinc (df, 2, 1816))


# In[17]:

list (df.ccode.unique())


# In[18]:

df.ccode.nunique()


# In[19]:

df.ccode.value_counts()


# In[ ]:



