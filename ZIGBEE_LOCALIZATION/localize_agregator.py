# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:26:38 2020

@author: Paul Vincent Nonat
"""
import numpy as np

RSSI_strings=np.empty(4, dtype='object')

message ="ref-node1:node1_0.100575 node2_0.109614 node3_0.123614"

if message.find("ref-node1:",0,10) !=-1: #spit the transmitted message from reference node
    RSSI_strings[0]= message.split(" ",-1)
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)

message ="ref-node2:node1_0.100575 node2_0.109614 node3_0.123614"

if message.find("ref-node1:",0,10) !=-1:
    RSSI_strings[0]= message.split(" ",-1)
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)


message ="ref-node3:node1_0.100575 node2_0.109614 node3_0.123614"

if message.find("ref-node1:",0,10) !=-1:
    RSSI_strings[0]= message.split(" ",-1)
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)

message ="ref-node4:node1_0.100575 node2_0.109614 node3_0.123614"

if message.find("ref-node1:",0,10) !=-1:
    RSSI_strings[0]= message.split(" ",-1)
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)

for x in range(RSSI_strings.size):
    for y in range(len(RSSI_strings[x])):
        RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
        RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
        
#RSSI_strings[x][y][z] x- reference node, y - node number z-always set to 1
        
#headers=['D1','D2','D3','D4','x','y']
#df= pd.read_csv('rss_experiment.csv',names=headers)
#
#actual_x=df['x'].values
#actual_x=np.delete(actual_x,0)
#actual_x=actual_x.astype('float64')
#actual_y=df['y'].values
#actual_y=np.delete(actual_y,0)
#actual_y=actual_y.astype('float64')

ref_node=np.array([[2,2],[-2,2],[-2,-2],[2,-2]]) #reference node coordinates in m from the center
for n in range(len(RSSI_strings[0])):
    X=np.array([[2*(ref_node[0][0]-ref_node[3][0]),2*(ref_node[0][1]-ref_node[3][1])],
                [2*(ref_node[1][0]-ref_node[3][0]),2*(ref_node[1][1]-ref_node[3][1])],
                [2*(ref_node[2][0]-ref_node[3][0]),2*(ref_node[2][1]-ref_node[3][1])]])
    a=np.array([
    [(pow(ref_node[0][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[0][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/RSSI_strings[0][n][1]),2)+pow(np.sqrt(1/RSSI_strings[3][n][1]),2))],
    [(pow(ref_node[1][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[1][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/RSSI_strings[1][n][1]),2)+pow(np.sqrt(1/RSSI_strings[3][n][1]),2))],
    [(pow(ref_node[2][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[2][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/RSSI_strings[2][n][1]),2)+pow(np.sqrt(1/RSSI_strings[3][n][1]),2))]])
    xy=a/X
    x,y=xy[2][0],xy[0][1]

    print("node=",n,"x=",x,"y=",y)