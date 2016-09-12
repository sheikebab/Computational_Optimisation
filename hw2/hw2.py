
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
import geoplotter as gp


# In[2]:

init = gp.GeoPlotter()
print(init.drawWorld())


# In[3]:

dv = init.readShapefile('cshapes_0.4-2/cshapes','darth_vader')


# In[12]:

cnty = init.m.darth_vader_info
dv_shape = init.m.darth_vader
# print dv_shape


# In[13]:

import pandas as pd


# In[14]:

shape_info = pd.DataFrame(cnty)


# In[15]:

shape_info.head()


# In[18]:

idx = shape_info.loc[:,'COWCODE'] == 2
# print idx


# In[19]:

init.drawShapes('darth_vader', idx)


# In[10]:

shapes_US = np.array()
for i in idx:
    
    

