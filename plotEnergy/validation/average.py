#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd
folder_list = ['1_15', '1_19', '1_24', '1_28', '2_15', '2_28', '3_17', '3_22', '5_15', '5_20', '8_8', '10_10', '12_12', '15_1', '15_2', '15_5', '15_15', '17_3', '19_1', '20_5', '22_3', '24_1', '28_1', '28_2']
with open('results.txt', 'a') as res_fid:
    for fd in folder_list:
        dframe = pd.read_csv(f"{fd}/Delta.energy-0", header=None)
        meanval = np.mean(dframe[0])
        median = np.median(dframe[0])
        res_fid.write(f"{fd} {meanval} {median}\n")


# In[ ]:




