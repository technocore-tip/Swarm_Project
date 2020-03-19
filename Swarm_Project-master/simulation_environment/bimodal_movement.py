# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 12:49:18 2020

@author: Paul Vincent Nonat
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 10:34:38 2020

@author:Rowel S Facunla
"""
from graphics import *
from environment import draw_windows,draw_swarm,distance_magnitude,relative_distance,update_pairwisedistance,position_vector
import time
import threading
import math
from random import *
import random
import seaborn as sns
import numpy as np
from itertools import combinations

import scipy.stats
import matplotlib.pyplot as plt


def mt_shuffle():
    np.random.shuffle(pairwise_list)

def bimodal_distribution(rho_bar1,sigma1,rho_bar2,sigma2,N,split1,split2):
    dist1=list()
    dist2=list()

        
    while(len(dist1)!=N*split1):
        s=np.random.normal(rho_bar1,sigma1)
        if s>=0:
            dist1.append(s)
    
    while(len(dist2)!=N*split2):
        s=np.random.normal(rho_bar2,sigma2)
        if s>=0:
            dist2.append(s)
    
    rho_k =dist1 +dist2
    plt.hist(rho_k,30,density=True)
    sns.distplot(rho_k, hist=False)
    plt.show()
    return rho_k


N=1000
mu=100
times=pow(2,-8)

rho_bar1=100
rho_bar2=300
sigma1=0
sigma2=0
split1=0.5
split2=0.5

rho_k = bimodal_distribution(rho_bar1,sigma1,rho_bar2,sigma2,N,split1,split2)
particles=list()

win = draw_windows(1024,1024) #draw window with width = 700 and height = 600.
robots = draw_swarm(N,win,1) #draw N swarm in win
win.getMouse() #blocking call

for i in range(1,N+1,1):
    particles.append([i,rho_k[i-1]])


#pairwise_list= list(combinations(particles,2))
pairwise_list = random.sample(particles, 2)
#mt_shuffle()

step=0

while(1): #replace with energy function
    pairwise_list = random.sample(particles, 2)
    robot_j = robots[pairwise_list[0][0]-1]
    rho_j= pairwise_list[0][1]
    robot_k= robots[pairwise_list[1][0]-1]
    rho_kk = pairwise_list[1][1]
    xj,yj,xk,yk,x_newj,y_newj,x_newk,y_newk=update_pairwisedistance(robot_j,rho_j,robot_k,rho_kk,times,mu,win)
    robot_j.move(xj,yj)
    #robot_k.move(xk,yk)
    #for z in range(len(pairwise_list)):
    #    pairwise_list = random.sample(particles, 2)
    #    robot_j = robots[pairwise_list[0][0]-1]
    #    rho_j= pairwise_list[0][1]
    #    robot_k= robots[pairwise_list[1][0]-1]
    #    rho_kk = pairwise_list[1][1]
#        print(robots[pairwise_list[z][0][0]-1])
#        print(robots[pairwise_list[z][1][0]-1])
    #    xj,yj,xk,yk,x_newj,y_newj,x_newk,y_newk=update_pairwisedistance(robot_j,rho_j,robot_k,rho_kk,times,mu,win)
        #time.sleep(100)
        #robots[pairwise_list[z][0][0]-1].move(xj + win.getWidth()/2,(win.getHeight()/2) - yj) # move bot to new position
        #robots[pairwise_list[z][1][0]-1].move(xk + win.getWidth()/2,(win.getHeight()/2) - yk)
    #    robot_j.move(xj,yj) # move bot to new position
    #    print(xj)
    #    print(yj)
        #robot_k.move(xk,yk)
        #print(robots[pairwise_list[z][0][0]-1])
        #print(robots[pairwise_list[z][1][0]-1])
        #print("Interaction : %d Step: %d",z,step)
        #print(z)
        #print(pairwise_list[z])
        #robots[pairwise_list[0][0]-1] = Circle(Point(x_newj+xj,y_newj+yj),2)
        #robots[pairwise_list[1][0]-1] = Circle(Point(x_newk+xk,y_newk+yk),2)
    #win.getMouse()
    #mt_shuffle()
    #step=1
