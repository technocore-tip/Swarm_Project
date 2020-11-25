# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 12:33:24 2020

@author: Paul Vincent Nonat
"""

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from random import randrange, uniform
import random
trial_name="SOL3-T5-POS3-N200.csv"
trial_name_wo="SOL3-T5-POS3_wo-N200.csv"
df=pd.read_csv(trial_name,header=None)#.values.astype('float64')
df=df.iloc[1:].values.astype('float64')

robot_no=list()
x=list()
y=list()
rho=list()
for z in range(len(df)):
    robot_no.append(df[z][0])
    x.append(df[z][1])
    y.append(df[z][2])
    rho.append(df[z][3])
print("before randomization")
print(rho)
random.shuffle(rho)
print("after randomization")
print(rho)

with open(trial_name_wo,mode='w',newline='') as csv_file:
    fieldnames =['robot_no','x','y','rho']
    writer = csv.DictWriter(csv_file,fieldnames=fieldnames)

    writer.writeheader()
    for q in range(len(df)):
        writer.writerow({'robot_no':robot_no[q],'x':x[q],'y':y[q],'rho':rho[q]})
