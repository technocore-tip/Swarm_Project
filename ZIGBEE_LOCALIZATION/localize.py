# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:26:38 2020

@author: Paul Vincent Nonat
"""
import pandas as pd
import numpy as np

#                         x1,y1 x2 y2  x3 y3   x4 y 
headers = ['d1','d2','d3','d4']
df = pd.read_csv('experiment.csv',names=headers)

d=[2.150581317,2.573907535,3.553167601,3.259601203]
ref_node=np.array([[2,2],[-2,2],[-2,-2],[2,-2]])
X=np.array([[2*(ref_node[0][0]-ref_node[3][0]),2*(ref_node[0][1]-ref_node[3][1])],
            [2*(ref_node[1][0]-ref_node[3][0]),2*(ref_node[1][1]-ref_node[3][1])],
            [2*(ref_node[2][0]-ref_node[3][0]),2*(ref_node[2][1]-ref_node[3][1])]])
a=np.array([
[(pow(ref_node[0][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[0][1],2)-pow(ref_node[3][1],2)-pow(d[0],2)+pow(d[3],2))],
[(pow(ref_node[1][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[1][1],2)-pow(ref_node[3][1],2)-pow(d[1],2)+pow(d[3],2))],
[(pow(ref_node[2][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[2][1],2)-pow(ref_node[3][1],2)-pow(d[2],2)+pow(d[3],2))]])