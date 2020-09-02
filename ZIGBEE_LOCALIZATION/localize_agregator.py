# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:26:38 2020

@author: Paul Vincent Nonat
"""
import time
#from line_plotter import AverageMeter, VisdomLinePlotter
import threading
import math
from random import *
import random

import numpy as np
from itertools import combinations
from pairwise_actions import distance_vector,distance_magnitude,update_pairwisedistance

import csv

RSSI_strings=np.empty(4, dtype='object')
RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""
message ="ref-node1: 1_0.132275791 2_0.157753005 3_0.088932425"

if message.find("ref-node1:",0,10) !=-1: #spit the transmitted message from reference node
    RSSI_strings[0]= message.split(" ",-1)
    del RSSI_strings[0][0]
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
    del RSSI_strings[1][0]
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
    del RSSI_strings[2][0]
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)
    del RSSI_strings[3][0]

message ="ref-node2: 1_0.134349434 2_0.217950277 3_132102382"
if message.find("ref-node1:",0,10) !=-1: #spit the transmitted message from reference node
    RSSI_strings[0]= message.split(" ",-1)
    del RSSI_strings[0][0]
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
    del RSSI_strings[1][0]
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
    del RSSI_strings[2][0]
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)
    del RSSI_strings[3][0]

message ="ref-node3: 1_0.12700944 2_0.100559174 3_0.224631531"

if message.find("ref-node1:",0,10) !=-1: #spit the transmitted message from reference node
    RSSI_strings[0]= message.split(" ",-1)
    del RSSI_strings[0][0]
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
    del RSSI_strings[1][0]
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
    del RSSI_strings[2][0]
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)
    del RSSI_strings[3][0]

message ="ref-node4: 1_0.132906608 2_0.079670311 3_0.117699689"

if message.find("ref-node1:",0,10) !=-1: #spit the transmitted message from reference node
    RSSI_strings[0]= message.split(" ",-1)
    del RSSI_strings[0][0]
if message.find("ref-node2:",0,10) !=-1:
    RSSI_strings[1]=  message.split(" ",-1)
    del RSSI_strings[1][0]
if message.find("ref-node3:",0,10) !=-1:
    RSSI_strings[2]=  message.split(" ",-1)
    del RSSI_strings[2][0]
if message.find("ref-node4:",0,10) !=-1:
    RSSI_strings[3]=  message.split(" ",-1)
    del RSSI_strings[3][0]

for x in range(RSSI_strings.size):
    for y in range(len(RSSI_strings[x])):
        RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
        RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
        RSSI_strings[x][y][0]=int(RSSI_strings[x][y][0])
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
robots =list()
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
    from_origin = np.sqrt(pow(x,2)+pow(y,2))
    robots.append((RSSI_strings[0][n][0],x,y,from_origin))
    print("node=",n,"x=",x,"y=",y)

def normal_distribution(mu,sigma,N):
    start_time = time.time()
    rho_k=list()
    while (len(rho_k)!=N):

        s= np.random.normal(sigma,mu)
        if s >= 0:
            rho_k.append(s)
  #  plt.hist(rho_k,30,density = True)
#    plotter.plot_histogram('Frequency','rho_k','Preferred distance histogram',np.asarray(rho_k, dtype=np.float32))
    #plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))
    return rho_k
N=3
rho_bar, sigma =10,1
mu=100
l=5*rho_bar
times=pow(2,-8)
rho_k = normal_distribution(rho_bar,sigma,N)
robotjk = random.sample(robots,2)
xj,yj,angle=update_pairwisedistance(robotjk[0][1],robotjk[0][2],rho_k[robotjk[0][0]-1],robotjk[1][1],robotjk[1][2],rho_k[robotjk[1][0]-1],times,mu)
def takefourth(elem):
    return elem[3]
#save initialize to CSV
#get robot distance from 
    
robots.sort(key=takefourth)
rho_k.sort()
sorted_robotlist=list()
for x in range(len(robots)): #reconstruct a list with its prefered distance
    sorted_robotlist.append((robots[x][0],robots[x][1],robots[x][2],rho_k[x])) #robot number, x,y,

sorted_robotlist.sort()
with open('test.csv',mode='w',newline='') as csv_file:
    fieldnames =['robot_no','x','y','rho']
    writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
    
    writer.writeheader()
    for x in range(len(sorted_robotlist)):
        writer.writerow({'robot_no':sorted_robotlist[x][0],'x':sorted_robotlist[x][1],'y':sorted_robotlist[x][2],'rho':sorted_robotlist[x][3]})

