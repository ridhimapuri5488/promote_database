#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[4]:


import pandas as pd
from io import StringIO

s=str(body,'utf-8')
data = StringIO(s) 
main = pd.read_csv(data)


# In[5]:


main.head(10)


# In[7]:


group_data = main.groupby('redcap_event_name')[['id_participant_l']].count()
group_data


# In[9]:


main[main["id_participant_l"] == "PRT170003"]

