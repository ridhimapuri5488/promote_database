#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


input_pre = 'csv_files/input_files/'
output_pre = 'csv_files/output_files/' 
main = pd.read_csv(input_pre + 'main.csv')
print(main.shape)


# In[3]:


group_data = main.groupby('redcap_event_name')[['id_participant']].count()
group_data


# In[4]:


list_events = main['redcap_event_name'].unique()
list_events


# In[5]:


for event in list_events:
    data = main[main['redcap_event_name'] == event]
    data.to_csv(output_pre + event + ".csv")
    
consent_files = [x for x in list_events if 'consent_initial' in x]

for f in consent_files:
    arm = pd.read_csv(output_pre + f + ".csv")
    arm_type = f.split('vi_')[-1]
    arm_files = [x for x in list_events if arm_type in x]
    for subfile in arm_files:
        sub =  pd.read_csv(output_pre + subfile + ".csv")
        print(sub.shape)
        print(sub.isnull().sum())
        sub.set_index('id_participant', inplace=True)
        sub.update(arm.set_index('id_participant'),overwrite=False)
        sub.reset_index()
        sub.to_csv(output_pre + subfile+ ".csv")


# ### Merging
# 

# In[6]:


mainfile = pd.read_csv(output_pre + list_events[0] + '.csv')
other_files = list_events[1:]
for file in other_files:
    subfile = pd.read_csv(output_pre + file + ".csv")
    mainfile = pd.concat([mainfile, subfile],sort=False)


# In[7]:


mainfile.shape


# In[8]:


mainfile.to_csv(output_pre + "promote_database.csv")


# In[ ]:




