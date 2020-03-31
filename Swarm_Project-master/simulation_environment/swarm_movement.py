# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 12:49:18 2020

@author: Paul Vincent Nonat, :Rowel S Facunla
"""

# -*- coding: utf-8 -*-
from graphics import *
from environment import draw_windows,draw_swarm,distance_magnitude,relative_distance,update_pairwisedistance,position_vector, total_relativedistance
import time
import threading
import math
from random import *
import random

import numpy as np
from itertools import combinations

import scipy.stats
import matplotlib.pyplot as plt


def mt_shuffle():
    np.random.shuffle(pairwise_list)

def normal_distribution(mu,sigma):
    start_time = time.time()
    rho_k=list()
    while (len(rho_k)!=N):

        s= np.random.normal(sigma,mu)
        if s >= 0:
            rho_k.append(s)
    plt.hist(rho_k,30,density = True)

    plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))
    return rho_k
simulation_time = time.time()

N=1000
rho_bar, sigma =0, 100
mu=100
l=5*rho_bar
times=pow(2,-8)

rho_k = normal_distribution(rho_bar,sigma)
particles=list()

win = draw_windows(1024,1024) #draw window with width = 700 and height = 600.
robots = draw_swarm(N,win,l) #draw N swarm in win
win.getMouse() #blocking call

for i in range(1,N+1,1):
    particles.append([i,rho_k[i-1]])


#pairwise_list= list(combinations(particles,2))
pairwise_list = random.sample(particles, 2)
#mt_shuffle()

step=0

rho_kmean =np.mean(rho_k)# second term of the energy function
combination= (N*(N-1))/2
U_knot=np.inf
U=np.inf
du=np.inf
epsilon= pow(10,-3)
while((np.abs(du))>epsilon): 
    interaction=1
    while(interaction!=combination):
        print("Interaction : %d Step: %d",interaction,step)
        pairwise_list = random.sample(particles, 2)
        robot_j = robots[pairwise_list[0][0]-1]
        rho_j= pairwise_list[0][1]
        robot_k= robots[pairwise_list[1][0]-1]
        rho_kk = pairwise_list[1][1]
        xj,yj,xk,yk,x_newj,y_newj,x_newk,y_newk=update_pairwisedistance(robot_j,rho_j,robot_k,rho_kk,times,mu,win)
        robot_j.move(xj,yj)
        interaction = interaction+1
        print("du/dt",du)
    if step==0:
        total_relativedist=total_relativedistance(robots,win,N)
        averageinterparticledist= (1/combination)*total_relativedist
        U_knot= averageinterparticledist- rho_kmean
        U=U_knot
        du=U
    if step>0:
        total_relativedist=total_relativedistance(robots,win,N)
        averageinterparticledist= (1/combination)*total_relativedist
        U= averageinterparticledist- rho_kmean
        du=U-U_knot
        U_knot=U
    
    step = step+1
total_time = time.time()-simulation_time
print("total runtime: " %d,total_time)
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
