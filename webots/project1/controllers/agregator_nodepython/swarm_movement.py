# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 12:49:18 2020

@author: Paul Vincent Nonat
"""

# -*- coding: utf-8 -*-
import concurrent.futures
from graphics import *
from environment import draw_windows,draw_swarm,distance_magnitude,relative_distance,update_pairwisedistance,position_vector, total_relativedistance,init_uniform_rhok,draw_robots
import csv
import time
from line_plotter import AverageMeter, VisdomLinePlotter
import threading
import math
from random import *
import random
import webcolors
import numpy as np
from itertools import combinations,permutations
import argparse

import scipy.stats
import matplotlib.pyplot as plt

import os
	
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

def mt_shuffle(step):
	np.random.seed(step)
	np.random.shuffle(pairwise_list)

def normal_distribution_color(rho_k):
    cm = plt.cm.get_cmap('RdYlBu_r')
    n,bins,patches=plt.hist(rho_k,30,density = True)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    print(patches)
    plotter.plot_histogram('Frequency','rho_k',trial_no+'Preferred distance histogram',np.asarray(rho_k, dtype=np.float32))
    col = bin_centers #- min(bin_centers)
    #col /= max(col)

    for c, p in zip(col, patches):
        plt.setp(p,fc=(cm(c/max(col))[0],cm(c/max(col))[1],cm(c/max(col))[2],1))
    plt.xlabel(r'Prefered Distance $\rho_k$')
    plt.ylabel(r'Probability')
    plt.savefig(trial_no+'.png', dpi=600)
    plt.show()
    return 0.5 * (bins[:-1] + bins[1:])

def interaction(z):
    robot_j = robots[pairwise_list[z][0][0]-1]
    rho_j= pairwise_list[z][0][1] #pair number
    robot_k= robots[pairwise_list[z][1][0]-1]
    rho_kk = pairwise_list[z][1][1]
    xj,yj=update_pairwisedistance(robot_j,rho_j,robot_k,rho_kk,times,mu,win,robots)
    robot_j.move(xj,yj)
    #return xj,yj
    #robot_j.move(xj,yj)




if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="--N [Number of Robots], --trial-name [trial name]")
	parser.add_argument('--N-robots',type=int,default=100,help='Number of Robots')
	parser.add_argument('--trial-name',type=str,required=True)
	args = parser.parse_args()
	N=args.N_robots
	trial_no=str(args.trial_name)
	plotter = VisdomLinePlotter(env_name="pairwise_experiment")
	simulation_time = time.time()
	if not os.path.exists(trial_no):
		os.makedirs(trial_no)
	#trial_no="WEBOTS-SOL3-T1"

	#N=100

	mu=100
	times=pow(2,-8)
	#rho_k,patches = normal_distribution(rho_bar,sigma,trial_no)

	particles=list()

	w,h=1024,1024
	win = draw_windows(1024,1024,str(trial_no)) #draw window with width = 700 and height = 600.

	robots,rho_k = draw_swarm(N,win,trial_no) #draw N swarm in win
	#robots,rho_k = init_uniform_rhok(rho_k,robots,1024,1024,win)
	patches=normal_distribution_color(rho_k)
	robots = draw_robots(N,win,robots,rho_k,patches)
	win.getMouse() #blocking call.

	for i in range(1,N+1,1):
		particles.append([i,rho_k[i-1]])
	pairwise_list= list(permutations(particles,2))
	#pairwise_list = random.sample(particles, 2)
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

	while(((np.abs(du))>epsilon) and ((np.abs(dUma))>epsilon)):
		objective_func = AverageMeter()
		averageobjective_func= AverageMeter()
		#previous Uma

		#interaction=1

		#while(interaction!=combination):

			#print("Interaction : %Step: %d",interaction,step)
		mt_shuffle(step)
		x_points=list()
		y_points=list()

		  #  print("du/dt",du)
		if step==0:
			print("time step:",step)
			for q in range (int(combination)):
				print("time step:",step,"Interaction :",q)
				interaction(q)
				with open(trial_no+'/'+trial_no+'-Step-'+str(step)+'-Interaction-'+str(q)+'.csv',mode='w',newline='') as csv_file:
					fieldnames =['robot_no','x','y','rho']
					writer = csv.DictWriter(csv_file,fieldnames=fieldnames)

					writer.writeheader()
					for w in range(len(rho_k)):
						x_coordinate=((robots[w].getCenter().getX()))-512
						y_coordinate=(((robots[w].getCenter().getY())-(h/2))*-1)
						writer.writerow({'robot_no':w+1,'x':x_coordinate,'y':y_coordinate,'rho':rho_k[w]})

			total_relativedist=total_relativedistance(robots,win,N)
			averageinterparticledist= (1/combination)*total_relativedist
			U_knot= averageinterparticledist- rho_kmean
			U=U_knot
			du=U
			#xk,yk,x_newj,y_newj,x_newk,y_newk
			Uma.append(U) #average list
			Uma_knot=np.mean(Uma)

		if step>0:
			print("time step:",step)
			for q in range (int(combination)):
				print("time step:",step,"Interaction :",q)
				interaction(q)
				with open(trial_no+'/'+trial_no+'-Step-'+str(step)+'-Interaction-'+str(q)+'.csv',mode='w',newline='') as csv_file:
					fieldnames =['robot_no','x','y','rho']
					writer = csv.DictWriter(csv_file,fieldnames=fieldnames)

					writer.writeheader()
					for w in range(len(rho_k)):
						x_coordinate=((robots[w].getCenter().getX()))-512
						y_coordinate=(((robots[w].getCenter().getY())-(h/2))*-1)
						writer.writerow({'robot_no':w+1,'x':x_coordinate,'y':y_coordinate,'rho':rho_k[w]})

			total_relativedist=total_relativedistance(robots,win,N)
			averageinterparticledist= (1/combination)*total_relativedist
			U= averageinterparticledist- rho_kmean
			du=U-U_knot

			U_knot=U
			Uma_knot=np.mean(Uma)
			Uma.append(U) #average List
			plotter.plot('U', 'U(t)', trial_no+'Objective Function',step, float(U))
			plotter.plot('U', 'U ma', trial_no+'Objective Function',step, float(np.mean(Uma)))

			plotter.plot('du/dt', 'dU/dt', trial_no+'Objective Function',step, float(du))

			
		if len(Uma)==32: #pop the oldest value of the running average
			dUma=np.mean(Uma)-Uma_knot
			plotter.plot('du/dt', 'd Uma/dt', trial_no+'Objective Function',step, float(dUma))
			del Uma[0]

		#robot_j.move(xj,yj)
		step = step+1

	total_time = time.time()-simulation_time
	print("total runtime: %d ",total_time)
	win.getMouse() #blocking call
