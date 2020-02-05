from graphics import * #using library from mcsp.wartburg.edu/zelle/python/graphics.py
import time
import threading
import math
from random import randint
import numpy as np

lock = threading.Lock()

def draw_windows(w,h): #function for creating the simulation space
	#create windows
	#print('create windows with name : swarm, width : ',w,', height : ',h)
	return GraphWin('swarm',w,h)
	pass

def draw_swarm(n,win,l): #function for drawing robot nodes
	robot =[]
	for x in range(0,n):
		#robot.append(Circle(Point( randint(20,win.getWidth-20) , randint(20,win.getHeight()-20) ), 0.5))
		robot.append(Circle(Point( randint(-(win.getWidth()/4),win.getWidth()/4)+win.getWidth()/2, (win.getHeight()/2)-randint(-(win.getHeight()/4),win.getHeight()/4) ), 2))
		#print(robot)
		#print('create robot with number ',x,' point x : ',x*200+40,', y : 200 , r : 5')
		robot[x].setFill('blue')
		robot[x].draw(win)
		pass
	#print(robot)
	return robot
	pass

#def stopping_condition(N,rho_k):


def distance_vector(P1,P2,win):#function to calculate distance between two points
    x1= P1.getX() - win.getWidth()/4 #win.getWidth()2 translate the given points to cartseian plane with origin at center of the plane instead at the side of window
    x2 = P2.getX() - win.getWidth()/4

    y1=win.getHeight()/2 - P1.getY()
    y2=win.getHeight()/2 - P2.getY()

    x = x1 - x2 #P1.getX()-P2.getX()
    y = y1 - y2 #P1.getY()-P2.getY()
    return x,y
    pass

def position_vector(P,win):
    x = P.getX() - win.getWidth()/4
    y = win.getHeight()/4 - P.getY()
    return x,y

def distance_magnitude(x,y):
	#calculate magnitude of distance vector
	return math.sqrt(x*x+y*y)
	pass

def relative_distance(robot,robots,win):#calculate relative distance of a robot to all other robots
	x_total=0
	y_total=0
	for r in robots:
		x,y = distance_vector(robot.getCenter(),r.getCenter())
		x_total+=x
		y_total+=y
		pass
	return x_total,y_total

def update_pairwisedistance(robot_j,rho_j,robot_k,rho_k,times,mu,win):
	x_p,y_p = distance_vector(robot_j.getCenter(),robot_k.getCenter(),win) #xj-xk , yj-yk
	pdist = distance_magnitude(x_p,y_p) # |rj - rk|
#    print("distance_vector")
#    print(x_p)
#    print(y_p)
#    print("Attraction Repulsion")
#    print("Theta")
	if y_p >= 0 and x_p >= 0:
		theta= np.arctan(y_p/x_p)

	if x_p < 0 and y_p >= 0:
		theta=(np.pi/2)+ np.arctan(y_p/x_p)

	if x_p <= 0 and y_p <= 0:
		theta= (np.pi) +np.arctan(y_p/x_p)

	if x_p >= 0 and y_p < 0:
		theta= ((3*np.pi)/2) +np.arctan(y_p/x_p)

	#theta= np.arctan(y_p/x_p)
	#    print("J particle movement")
	xrj = mu*np.cos(theta)*math.tanh(pdist-rho_j)*times
	yrj = mu*np.sin(theta)*math.tanh(pdist-rho_j)*times
	#    print("K particle movement")
	xrk = mu*np.cos(theta)*math.tanh(pdist-rho_k)*times
	yrk = mu*np.sin(theta)*math.tanh(pdist-rho_k)*times
#    print("J Previous Pos")
	xj,yj= position_vector(robot_j.getCenter(),win)  #update position vectors
	#    print(xj)
	#    print(yj)
	#    print("J new Pos")
	xj= xj + xrj
	yj = yj + yrj
	#    print(xj)
	#    print(yj)
	#
	#    print("K Previous Pos")
	xk,yk= position_vector(robot_k.getCenter(),win)  #update position vectors
	#    print(xk)
	#    print(yk)
	xk= xk + xrk
	yk = yk + yrk
#    print("K new Pos")
#    print(xk)
#    print(yk)
	return xrj,yrj,xrk,yrk
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
