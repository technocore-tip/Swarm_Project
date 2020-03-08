# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 10:34:38 2020

@author: Paul Vincent Nonat
"""
from environment import draw_windows,draw_swarm,distance_magnitude,relative_distance,update_pairwisedistance,position_vector
import time
import threading
import math
from random import randint

import numpy as np
from itertools import combinations

import scipy.stats
import matplotlib.pyplot as plt


def mt_shuffle():
    np.random.shuffle(pairwise_list)
    
def normal_distribution(mu,sigma):
    rho_k=list()
    
    while (len(rho_k)!=N):
        
        s= np.random.normal(sigma,mu)
        if s > 0:
            rho_k.append(s)
    
    return rho_k
    plt.hist(rho_k,30,density = True)
    
    plt.show()

    
N=1000 #number of particles
rho_bar, sigma = 10, 0
mu=50
l=5*rho_bar
times=pow(2,-8)

rho_k = normal_distribution(rho_bar,sigma)
particles=list()



win = draw_windows(1024,1024) #draw window with width = 700 and height = 600.
robots = draw_swarm(N,win,l) #draw 7 swarm in win
win.getMouse() #blocking call

for i in range(1,N+1,1):
    particles.append([i,rho_k[i-1]])


pairwise_list= list(combinations(particles,2))
mt_shuffle()


step=0

while(1): #replace with energy function
    step= step+1
    for z in range(len(pairwise_list)):
        robot_j = robots[pairwise_list[z][0][0]-1]
        rho_j= pairwise_list[z][0][1]
        robot_k= robots[pairwise_list[z][1][0]-1]
        rho_k = pairwise_list[z][1][1]
#        print(robots[pairwise_list[z][0][0]-1])
#        print(robots[pairwise_list[z][1][0]-1])
        xj,yj,xk,yk=update_pairwisedistance(robot_j,rho_j,robot_k,rho_k,times,mu,win)

        #time.sleep(10)
        #robots[pairwise_list[z][0][0]-1].move(xj + win.getWidth()/2,(win.getHeight()/2) - yj) # move bot to new position
        #robots[pairwise_list[z][1][0]-1].move(xk + win.getWidth()/2,(win.getHeight()/2) - yk)
        robots[pairwise_list[z][0][0]-1].move(xj,-yj) # move bot to new position
        robots[pairwise_list[z][1][0]-1].move(xk,-yk)
#        print(robots[pairwise_list[z][0][0]-1])
#        print(robots[pairwise_list[z][1][0]-1])
        print("Interaction : %d Step: %d",z,step)
        print(z)
        print(pairwise_list[z])
        #win.getMouse()
   # win.getMouse()
    mt_shuffle()
