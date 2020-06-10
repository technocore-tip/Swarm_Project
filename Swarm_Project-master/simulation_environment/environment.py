from graphics import * #using library from mcsp.wartburg.edu/zelle/python/graphics.py
import time
import threading
import math
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import webcolors
#swarm environment
lock = threading.Lock()
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

def draw_windows(w,h): #function for crea.ting the simulation space
	#create windows
	#print('create windows with name : swarm, width : ',w,', height : ',h)
	return GraphWin('swarm',w,h)
	pass

def draw_swarm(n,win,l,rho_k,patches): #function for drawing robot nodes
    robot =[]
    max_p = max(patches)
    for x in range(0,n):
    		#robot.append(Circle(Point( randint(20,win.getWidth-20) , randint(20,win.getHeight()-20) ), 0.5))
        robot.append(Circle(Point( randint(-(win.getWidth()/4),win.getWidth()/4)+win.getWidth()/2, (win.getHeight()/2)-randint(-(win.getHeight()/4),win.getHeight()/4) ),4 ))
        		#print(robot)
        		#print('create robot with number ',x,' point x : ',x*200+40,', y : 200 , r : 5')
        cm = plt.cm.get_cmap('RdYlBu_r')
        actual_name, closest_name = get_colour_name((int(cm(rho_k[x]/max(rho_k))[0]*255),int(cm(rho_k[x]/max(rho_k))[1]*255),int(cm(rho_k[x]/max(rho_k))[2]*255)))
        #actual_name, closest_name = get_colour_name((int(cm((rho_k[x]/max(rho_k))-min(rho_k))[0]*255),int(cm((rho_k[x]/max(rho_k))-min(rho_k))[1]*255),int(cm((rho_k[x]/max(rho_k))-min(rho_k))[2]*255)))
        robot[x].setFill(closest_name)
        robot[x].draw(win)
    pass
    	#print(robot)
    return robot
    pass

#def stopping_condition(N,rho_k):


def distance_vector(P1,P2,win):#function to calculate distance between two points
    x1 = P1.getX()#  - win.getWidth()/2 
    #win.getWidth()2 translate the given points to cartseian plane with origin at center of the plane instead at the side of window
    x2 = P2.getX()# - win.getWidth()/2
    y1= P1.getY()# + win.getHeight()/2 
    y2= P2.getY()# + win.getHeight()/2

    x = x2 - x1 #P1.getX()-P2.getX()
    y = y2 - y1 #P1.getY()-P2.getY()
    return x,y
    pass

def position_vector(P,win):
    x = P.getX() + win.getWidth()/2
    y = P.getY() - win.getHeight()/2 
    return x,y

def distance_magnitude(x,y):
	#calculate magnitude of distance vector
	return math.sqrt((x*x)+(y*y))
	pass

def total_relativedistance(robots,win,N): # for energy function
    x_total=0
    y_total=0
    for j in range(N-1):
        for k in range(j+1,N,1):
            x,y=distance_vector(robots[j].getCenter(),robots[k].getCenter(),win)
            x_total +=x
            y_total+=y
    return distance_magnitude(x_total,y_total)

def relative_distance(robot,robots,win):#calculate relative distance of a robot to all other robots
	x_total=0
	y_total=0
	for r in robots:
		x,y = distance_vector(robot.getCenter(),r.getCenter())
		x_total+=x
		y_total+=y
		pass
	return x_total,y_total

def get_nearbybots(robot_j,robots,win,xrj,yrj,theta,beta):
    relative_dist=np.zeros((len(robots),4))
    
    i=0 
    near_robotlist=list()
    delta_r=distance_magnitude(xrj,yrj)
    for r in robots:
        relative_dist[i][0],relative_dist[i][1]= distance_vector(robot_j.getCenter(),r.getCenter(),win)
        relative_dist[i][2] = distance_magnitude(relative_dist[i][0],relative_dist[i][1])-8 # 4 is the diameter of the bot
              
        relative_dist[i][3]= calculate_angle(relative_dist[i][0],relative_dist[i][1])    #relative_dist[i][3] phi    
        
        if relative_dist[i][2] <= delta_r and ((theta-beta >= relative_dist[i][3]) and (theta+beta <= relative_dist[i][3])):
            near_robotlist.append(i)
        i = i+1
    
    
    if len(near_robotlist)==0: 
        return xrj, yrj
    
    z=0
    if len(near_robotlist)>1:
        for k in range(len(near_robotlist)):
            if k==0:
                temp=np.abs(theta-relative_dist[near_robotlist[k]][3])
                z=k
            if k>0:
                if np.abs(theta-relative_dist[near_robotlist[k]][3])<=temp:
                    temp=np.abs(theta-relative_dist[near_robotlist[k]][3])
                    z=k
        return relative_dist[near_robotlist[z]][2]*np.cos(relative_dist[near_robotlist[z]][3]),relative_dist[near_robotlist[z]][2]*np.sin(relative_dist[near_robotlist[z]][3])
    
    
    if len(near_robotlist)==1:
        return relative_dist[near_robotlist[0]][2]*np.cos(relative_dist[near_robotlist[0]][3]),relative_dist[near_robotlist[0]][2]*np.sin(relative_dist[near_robotlist[0]][3])
    

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

def update_pairwisedistance(robot_j,rho_j,robot_k,rho_k,times,mu,win,robots):
    x_p,y_p= distance_vector(robot_j.getCenter(),robot_k.getCenter(),win) #xj-xk , yj-yk
    pdist = distance_magnitude(x_p,y_p) # |rj - rk|
    theta= calculate_angle(x_p,y_p)
        
    deg = theta*180/np.pi
    
    #print(x_p, y_p, deg)
    
    xrj = mu*np.cos(theta)*math.tanh(pdist-rho_j)*times
    yrj = mu*np.sin(theta)*math.tanh(pdist-rho_j)*times
    print(xrj,yrj,distance_magnitude(xrj,yrj))
    #xrj,yrj=get_nearbybots(robot_j,robots,win,xrj,yrj,theta,(45*np.pi/180))
    return xrj,yrj#,xrk,yrk,xj,yj,xk,yk
	#calculate the pairwise distance



#def main():
#	#main program
#	win = draw_windows(1920,1080) #draw window with width = 700 and height = 600
#	robots = draw_swarm(1000,win) #draw 7 swarm in win
#	win.getMouse() #blocking call
#	simulate_meeting_point(robots) #start simulation meeting point
#	win.getMouse()
#	pass
#
#if __name__ == '__main__':
#	main()