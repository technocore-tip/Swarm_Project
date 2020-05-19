# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:26:38 2020

@author: Paul Vincent Nonat
"""
import pandas as pd
import numpy as np

headers=['D1','D2','D3','D4','x','y']
df= pd.read_csv('rss_experiment.csv',names=headers)

actual_x=df['x'].values
actual_x=np.delete(actual_x,0)
actual_x=actual_x.astype('float64')
actual_y=df['y'].values
actual_y=np.delete(actual_y,0)
actual_y=actual_y.astype('float64')

result=list()
error=list()
for n in range(1,df.shape[0],1):
    d=df.iloc[n].values.astype('float64')
    ref_node=np.array([[2,2],[-2,2],[-2,-2],[2,-2]])
    X=np.array([[2*(ref_node[0][0]-ref_node[3][0]),2*(ref_node[0][1]-ref_node[3][1])],
                [2*(ref_node[1][0]-ref_node[3][0]),2*(ref_node[1][1]-ref_node[3][1])],
                [2*(ref_node[2][0]-ref_node[3][0]),2*(ref_node[2][1]-ref_node[3][1])]])
    a=np.array([
    [(pow(ref_node[0][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[0][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/d[0]),2)+pow(np.sqrt(1/d[3]),2))],
    [(pow(ref_node[1][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[1][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/d[1]),2)+pow(np.sqrt(1/d[3]),2))],
    [(pow(ref_node[2][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[2][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/d[2]),2)+pow(np.sqrt(1/d[3]),2))]])
    xy=a/X
    x,y=xy[2][0],xy[0][1]
    rmse=np.sqrt(pow(actual_x[n-1]-x,2)+pow(actual_y[n-1]-y,2))
    result.append([x,y,rmse])
    error.append(rmse)
    print("Trial=",n,"x=",x,"y=",y,"RMSE=",rmse)