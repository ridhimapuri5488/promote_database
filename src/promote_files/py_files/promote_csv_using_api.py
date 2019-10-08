#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pycurl
import io
from urllib.parse import urlencode
import pandas as pd

data = {
    'token': '89DCF6943B10616B328CA2C3AE068CF0',
    'content': 'record',
    'format': 'csv',
    'type': 'flat',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

buf = io.BytesIO()
ch = pycurl.Curl()
ch.setopt(ch.URL, "https://www.ctsiredcap.pitt.edu/redcap/api/")

postfields = urlencode(data)
ch.setopt(ch.POSTFIELDS, postfields)
#ch.setopt(ch.POST, data.items())

ch.setopt(ch.WRITEFUNCTION, buf.write)
ch.perform()
ch.close()


body = buf.getvalue()
#print(body)


# In[2]:


type(body)


# In[3]:


from io import StringIO

s=str(body,'utf-8')
data = StringIO(s) 
main = pd.read_csv(data)


# In[4]:


main.head(10)


# In[5]:


group_data = main.groupby('redcap_event_name')[['id_participant']].count()
group_data


# In[6]:


list_events = main['redcap_event_name'].unique()
list_events


# In[7]:


output_pre = '../' 
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
        #sub.to_csv(subfile+ ".csv")


# In[8]:


mainfile = pd.read_csv(output_pre + list_events[0] + '.csv')
other_files = list_events[1:]
for file in other_files:
    subfile = pd.read_csv(output_pre + file + ".csv")
    mainfile = pd.concat([mainfile, subfile],sort=False)


# In[9]:


mainfile.shape
list(mainfile)


# In[10]:


del mainfile['Unnamed: 0']
list(mainfile)


# In[11]:


mainfile.head(20)


# In[12]:


mainfile.to_csv(output_pre + "promote_database.csv")
#mainfile.to_csv("promote_database.csv")


# In[15]:


import pycurl
import io
from urllib.parse import urlencode

data = {
    'token': 'F9DD295357CE8FAC8062B80E85DF5063',
    'content': 'record',
    'format': 'csv',
    'type': 'flat',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

buf = io.BytesIO()
ch = pycurl.Curl()
ch.setopt(ch.URL, "https://www.ctsiredcap.pitt.edu/redcap/api/")

postfields = urlencode(data)
ch.setopt(ch.POSTFIELDS, postfields)
#ch.setopt(ch.POST, data.items())

ch.setopt(ch.WRITEFUNCTION, buf.write)
ch.perform()
ch.close()


body = buf.getvalue()
#print(body)
import pandas as pd
from io import StringIO

s=str(body,'utf-8')
data = StringIO(s) 
main = pd.read_csv(data)
main.to_csv(output_pre + "longitudinal.csv")

