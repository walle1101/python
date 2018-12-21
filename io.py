#!/usr/bin/env python
import numpy as np
import pandas as pd
import time,sys,os,pickle
io = pd.read_csv(sys.argv[1],skiprows=[0],sep='\s+').groupby('Device:') 
num = io['Device:'].value_counts()['sda'] 
p1 = pd.DataFrame(np.arange(int(num)))
for i,j in io: 
    j=j['MB_read/s'].reset_index(drop=True) 
    k=pd.DataFrame(j) 
    k.columns=[i] 
    p1 = p1.join(k) 
p1.iloc[:,2:].astype(float).to_excel('io.xlsx')

