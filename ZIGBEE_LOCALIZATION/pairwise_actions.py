# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:04:31 2020

@author: Paul Vincent Nonat
"""

import time
import threading
import math
from random import randint
import numpy as np

def distance_vector(x1,y1,x2,y2):#function to calculate distance between two points

    x = x2 - x1 #P1.getX()-P2.getX()
    y = y2 - y1 #P1.getY()-P2.getY()
    return x,y
    pass

def distance_magnitude(x,y):
	#calculate magnitude of distance vector
	return math.sqrt((x*x)+(y*y))
	pass

def calculate_angle(x_p,y_p):
    if x_p == 0 and y_p == 0: #1
        slope = 0
        theta= np.arctan(slope)
    if x_p >0 and y_p==0: #2
        theta=np.arctan(0)
    
    if x_p>0 and y_p>0: #3
        slope= np.abs(y_p/x_p)
        theta =np.arctan(slope)
    if x_p==0 and y_p>0: #4
        theta = (np.pi)/2
    if x_p < 0 and y_p > 0: #5
        slope= np.abs(y_p/x_p)      
        theta = np.pi - np.arctan(slope)
    if x_p < 0 and y_p ==0: #6
        theta = np.pi
    if x_p < 0 and y_p < 0: #7
        slope= np.abs(y_p/x_p)    
        theta = np.pi + np.arctan(slope)
    if x_p == 0 and y_p < 0: #8
        theta = (3*np.pi)/2
    if x_p > 0 and y_p < 0:
        slope= np.abs(y_p/x_p)
        theta = (2*np.pi) - np.arctan(slope)
    
    return theta

def update_pairwisedistance(xj,yj,rho_j,xk,yk,rho_k,times,mu):
    x_p,y_p= distance_vector(xj,yj,xk,yk) #xj-xk , yj-yk
    pdist = distance_magnitude(x_p,y_p) # |rj - rk|
    theta= calculate_angle(x_p,y_p)
        
    deg = theta*180/np.pi
    
    print(x_p, y_p, deg)

    xrj = mu*np.cos(theta)*math.tanh(pdist-rho_j)*times
    yrj = mu*np.sin(theta)*math.tanh(pdist-rho_j)*times

    return xrj,yrj,theta#,xrk,yrk,xj,yj,xk,yk
	#calculate the pairwise distance
