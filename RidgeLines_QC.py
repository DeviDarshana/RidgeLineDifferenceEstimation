#!/usr/bin/env python
# coding: utf-8

# # Required Modules

# In[35]:


import csv
import math
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from ast import literal_eval
from io import StringIO


# # Methods

# In[38]:


# method to make list of list

def process_file(file):
    groups = [[]]
    for line in file:
        if (line != '\n'):
            groups[-1].append(line)  
        else:
            groups.append([])
    return groups


def convert_to_float(test_list):
    test_list = [float(i) for i in test_list]
    return test_list

def calculate_points(midpoint,start,end):          # midpoint is a single value, start and end are passed as lists
    for l in range (len(end)):
        ap = (midpoint-(start[l]))
        ab = ((end[l])-(start[l]))
        answer = (np.dot(ap,ab)/np.dot(ab,ab))
        answer1 = answer * ab
        answer_fin = (s_start[l] + answer1)  
        
def ClosestPointOnLine(a, b, p):
    ap = p-a
    ab = b-a
    firstdot = np.dot(ap,ab)
    seconddot = np.dot(ab,ab)
    divdot = firstdot/seconddot
    r = (a + ((divdot) * ab))
    return r


# # Main

# In[ ]:


with open('input.txt', 'r') as file:
    l = process_file(file)


# In[43]:


# to make list of list of dictionary

keys = ['scanline','start','end']
emptylist=[]
result=[]
for i in l:
    for j in i[1:]:
        m=j.split(" ")
        result_dict ={}
        result_dict["scanline"] = m[0]
        result_dict[ "start"]= m[2:5]
        result_dict["end"]= m[5:8]
        emptylist.append(result_dict)
    result.append(emptylist)
    emptylist=[]


# In[44]:


# to call the midpoint method within the loop 

s=0
m=0
midpoint =[]
list1=[]
index=0
for i in result:
    a = result[s][0]['start']
    b = result[s][0]['end']
    c = result[s][0]['scanline']
    midpoint_values=[]
    for k in range(len(b)):
        mpoint= ((float(a[k])+float(b[k]))/2)
        midpoint_values.append(mpoint)
    midpoint.append(midpoint_values)
    for j in i[1:]:
        j['index'] = index
        j['m_start'] = a                                # start of midpoint's 
        j['m_end'] = b
        j['m_scanline']=c
        j['midpoint'] =midpoint_values
        list1.append(j)
    index=index+1
    s=s+1
    midpoint_values=[]
    m_val=[]


# In[45]:


mpoint = pd.DataFrame(midpoint)
mpoint.columns=['x','y','z']
# mpoint['x'][0]                          # calling x column, 1st row

df= pd.DataFrame(list1)

df['start'] = df['start'].apply(lambda x : pd.to_numeric(x))
df['end'] = df['end'].apply(lambda x : pd.to_numeric(x))

df['project_mp_on_second'] = df.apply(lambda row: ClosestPointOnLine(row['start'], row['end'], row['midpoint']), axis=1)
df['project_mp_on_second'] = df['project_mp_on_second'].apply(np.array)

grouped = df.groupby('index')

# for name,group in grouped:
#     print('\n')
#     print ("----------------at index ",name,"---------------")
#     print (group)
#     print (grouped['project_mp_on_second'].sum())
    
df2 = pd.DataFrame(df.project_mp_on_second.tolist()).groupby(df['index']).mean() 
df2.columns=['avg_x','avg_y','avg_z']

df3 = pd.merge(df, df2, how='outer', on=['index'])

df3['avg_midpoint'] = [[x, y,z] for x, y, z in zip(df3.avg_x, df3.avg_y, df3.avg_z)]

#Deleting the separate start points in x,y,z 
df3 = df3.drop(['avg_x','avg_y','avg_z'], axis=1)

#projecting avg midpoint again on other lines
df3['project_avg_on_other'] = df3.apply(lambda row: ClosestPointOnLine(row['start'], row['end'], row['avg_midpoint']), axis=1)

#diff between avg midpoint and projection on other
df3['diff_avg_other'] =  df3['project_avg_on_other'] - df3['avg_midpoint']

#split the diff_avg_other into 3 cols

df3[['fin_x','fin_y','fin_z']] = pd.DataFrame(df3.diff_avg_other.tolist(), index= df3.index)
df3[['avg_x','avg_y','avg_z']] = pd.DataFrame(df3.avg_midpoint.tolist(), index= df3.index)

#write output to csv file

df3.to_csv('output.csv')







