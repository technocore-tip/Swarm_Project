# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:41:52 2020

@author: Paul Vincent Nonat
"""
import threading
from graphics import *
from environment import draw_windows,draw_swarm,distance_magnitude,relative_distance,update_pairwisedistance,position_vector#, total_relativedistance

import time
#from line_plotter import AverageMeter, VisdomLinePlotter
import threading
import math
from random import *
import random

import numpy as np
from itertools import combinations

import scipy.stats
import matplotlib.pyplot as plt

lock = threading.Lock()
def mt_shuffle():
    np.random.shuffle(pairwise_list)

def normal_distribution(mu,sigma):
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

#plotter = VisdomLinePlotter(env_name="Swarm_Simulation")


#pairwise_list= list(combinations(particles,2))
#pairwise_list = random.sample(particles, 2)
#mt_shuffle()

step=0

#combination= (N*(N-1))/2

def robot_movement(robots,particles,robot_id,times,mu,win):
        lock.acquire()
        pairwise_list =random.sample(particles,1)
        robot_j = robots[particles[robot_id-1][0]-1]
        rho_j= particles[robot_id-1][1]
        robot_k = robots[pairwise_list[0][0]-1]
        rho_k = pairwise_list[0][1]
        
        xj,yj =update_pairwisedistance(robot_j,rho_j,robot_k,rho_k,times,mu,win,robots)
        lock.release()
        robot_j.move(xj,yj)

        
#while(1): 
#
#    
#    interaction=1
#
#    while(interaction!=combination):
#        print("Interaction : %d Step: %d",interaction,step)
#        pairwise_list = random.sample(particles, 2)
#        robot_j = robots[pairwise_list[0][0]-1]
#        rho_j= pairwise_list[0][1]
#        robot_k= robots[pairwise_list[1][0]-1]
#        rho_kk = pairwise_list[1][1]
#        xj,yj=update_pairwisedistance(robot_j,rho_j,robot_k,rho_kk,times,mu,win,robots)
#        robot_j.move(xj,yj)
#        interaction = interaction+1
def run_robbos(robots,win,N):
    trial_no="BD1"
    rho_bar, sigma =0, 100
    mu=100
    l=5*rho_bar
    times=pow(2,-8)
    
    rho_k = normal_distribution(rho_bar,sigma)

    particles=list()
    for i in range(1,N+1,1):
        particles.append([i,rho_k[i-1]]) 

    while(1):
        for i in range(1,N+1):
            worker = threading.Thread(target=robot_movement,args=(robots,particles,i,times,mu,win))
            print(worker)
            worker.setDaemon(True)
            worker.start()
            
#    step = step+1
if __name__ == '__main__':
    simulation_time = time.time()
    N=10
    l=5
    win = draw_windows(1024,1024) #draw window with width = 700 and height = 600.
    robots = draw_swarm(N,win,l) #draw N swarm in win
    
    win.getMouse() #blocking call
    run_robbos(robots,win,N)
    total_time = time.time()-simulation_time
    print("total runtime: %d ",total_time)
    win.getMouse() #blocking call