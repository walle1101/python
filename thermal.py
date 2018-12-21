#!/usr/bin/env python
import numpy as np
import pandas as pd
import time,sys,os,pickle
row = pd.read_csv(sys.argv[1]).shape[1]
td = pd.read_csv(sys.argv[1],names=range(row))
#td.T.iloc[2:].drop_duplicates(keep=False).reset_index(drop=True).to_excel('thermal.xlsx')
td[td!=0].T.iloc[2:].dropna(axis=0,how='all').reset_index(drop=True).fillna(0).to_excel('thermal.xlsx')
