# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 12:49:18 2020

@author: Paul Vincent Nonat
"""

# -*- coding: utf-8 -*-
from graphics import *
from environment import draw_windows,draw_swarm,distance_magnitude,relative_distance,update_pairwisedistance,position_vector, total_relativedistance,init_uniform_rhok,draw_robots

import time
#from line_plotter import AverageMeter, VisdomLinePlotter
import threading
import math
from random import *
import random
import webcolors
import numpy as np
from itertools import combinations

import scipy.stats
import matplotlib.pyplot as plt
#actual_name, closest_name = get_colour_name((int(cm(rho_k[x]/max(patches))[0]*255),int(cm(rho_k[x]/max(patches))[1]*255),int(cm(rho_k[x]/max(patches))[2]*255)))
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None 
    return actual_name, closest_name

def mt_shuffle():
    np.random.shuffle(pairwise_list)

def normal_distribution(mu,sigma,trial_no):
    start_time = time.time()
    rho_k=list()
    while (len(rho_k)!=N):

        s= np.random.normal(sigma,mu)
        if s >= 0:
            rho_k.append(s)
    cm = plt.cm.get_cmap('RdYlBu_r')
    n,bins,patches=plt.hist(rho_k,30,density = True)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    print(patches)
#    plotter.plot_histogram('Frequency','rho_k','Preferred distance histogram',np.asarray(rho_k, dtype=np.float32))
    col = bin_centers #- min(bin_centers)
    #col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p,fc=(cm(c/max(col))[0],cm(c/max(col))[1],cm(c/max(col))[2],1))
    plt.xlabel(r'Prefered Distance $\rho_k$')
    plt.ylabel(r'Probability')
    plt.savefig(trial_no+'.png', dpi=600)
    plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))
    return rho_k,0.5 * (bins[:-1] + bins[1:])

#plotter = VisdomLinePlotter(env_name="Swarm_Simulation")
simulation_time = time.time()

trial_no="With Uniform rho_k Initialization"

N=100
rho_bar, sigma =50,100
mu=100
l=5*rho_bar
times=pow(2,-8)
rho_k,patches = normal_distribution(rho_bar,sigma,trial_no)

particles=list()

    
win = draw_windows(1024,1024,trial_no) #draw window with width = 700 and height = 600.

robots = draw_swarm(N,win) #draw N swarm in win
robots,rho_k = init_uniform_rhok(rho_k,robots,1024,1024,win)
robots = draw_robots(N,win,robots,rho_k,patches)
win.getMouse() #blocking call

for i in range(1,N+1,1):
    particles.append([i,rho_k[i-1]])
#pairwise_list= list(combinations(particles,2))
pairwise_list = random.sample(particles, 2)
#mt_shuffle()

step=0

rho_kmean =np.mean(rho_k)# second term of the energy function
combination= (N*(N-1))/2
U_knot=0 #Order Parameter
U=0 #Order Parameter
du= (1/combination)*total_relativedistance(robots,win,N) - rho_kmean
U=du
epsilon= pow(9,-5)

Uma=list() #Order Parameter Running Average
Uma.append(du) #Average List
dUma=np.mean(Uma)
Uma_knot=0
while(1):#((np.abs(du))>epsilon and (np.abs(dUma))>epsilon): 
    #objective_func = AverageMeter()
    #averageobjective_func= AverageMeter()
    #previous Uma
    
    interaction=1
    #plotter.plot('U', 'U(t)', trial_no+'Objective Function',step, float(U))
    #plotter.plot('U', 'U ma', trial_no+'Objective Function',step, float(np.mean(Uma)))

    #plotter.plot('du/dt', 'dU/dt', trial_no+'Objective Function',step, float(du))
    
    while(interaction!=combination):
      #  print("Interaction : %d Step: %d",interaction,step)
        pairwise_list = random.sample(particles, 2)
        robot_j = robots[pairwise_list[0][0]-1]
        rho_j= pairwise_list[0][1]
        robot_k= robots[pairwise_list[1][0]-1]
        rho_kk = pairwise_list[1][1]
        xj,yj=update_pairwisedistance(robot_j,rho_j,robot_k,rho_kk,times,mu,win,robots)
        robot_j.move(xj,yj)
        interaction = interaction+1
      #  print("du/dt",du)
    if step==0:
        total_relativedist=total_relativedistance(robots,win,N)
        averageinterparticledist= (1/combination)*total_relativedist
        U_knot= averageinterparticledist- rho_kmean
        U=U_knot
        du=U
        #xk,yk,x_newj,y_newj,x_newk,y_newk
        Uma.append(U) #average list
        Uma_knot=np.mean(Uma)
        
    if step>0:
        total_relativedist=total_relativedistance(robots,win,N)
        averageinterparticledist= (1/combination)*total_relativedist
        U= averageinterparticledist- rho_kmean
        du=U-U_knot
        
        U_knot=U
        Uma_knot=np.mean(Uma)
        Uma.append(U) #average List

    if len(Uma)==32: #pop the oldest value of the running average
        dUma=np.mean(Uma)-Uma_knot
        #plotter.plot('du/dt', 'd Uma/dt', trial_no+'Objective Function',step, float(dUma))
        del Uma[0]
    
    step = step+1
    
total_time = time.time()-simulation_time
print("total runtime: %d ",total_time)
win.getMouse() #blocking call
