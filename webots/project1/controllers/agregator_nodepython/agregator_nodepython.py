from controller import Robot
from controller import Receiver, Emitter
import time
import numpy as np
from itertools import combinations
import struct
import random
from pairwise_actions import distance_vector,distance_magnitude,update_pairwisedistance
from numpy.lib import recfunctions as rfn
N=100
def normal_distribution(mu,sigma,N):
    start_time = time.time()
    rho_k=list()
    while (len(rho_k)!=N):

        s= np.random.normal(sigma,mu)
        if s >= 0:
            rho_k.append((10+s)) #3.55 is the radius of the robot body
  #  plt.hist(rho_k,30,density = True)
#    plotter.plot_histogram('Frequency','rho_k','Preferred distance histogram',np.asarray(rho_k, dtype=np.float32))
    #plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))
    return rho_k

def localize_robots(ref_node1,ref_node2,ref_node3,ref_node4):
	ref_node=np.array([[4,4],[-4,4],[-4,-4],[4,-4]])
	robots= list()
	robots.clear()
	for n in range(N):
		X=np.array([[2*(ref_node[0][0]-ref_node[3][0]),2*(ref_node[0][1]-ref_node[3][1])],
				[2*(ref_node[1][0]-ref_node[3][0]),2*(ref_node[1][1]-ref_node[3][1])],
				[2*(ref_node[2][0]-ref_node[3][0]),2*(ref_node[2][1]-ref_node[3][1])]])
		a=np.array([
		[(pow(ref_node[0][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[0][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/ref_node1[n][1]),2)+pow(np.sqrt(1/ref_node4[n][1]),2))],
		[(pow(ref_node[1][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[1][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/ref_node2[n][1]),2)+pow(np.sqrt(1/ref_node4[n][1]),2))],
		[(pow(ref_node[2][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[2][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/ref_node3[n][1]),2)+pow(np.sqrt(1/ref_node4[n][1]),2))]])
		xy=a/X
		x,y=xy[2][0]*100,xy[0][1]*100 #change unit to cm
		robots.append([ref_node1[n][0],x,y])
		#print("Real-Time Location (m):node=",n,"x=",x,"y=",y)
		#print(robots)
	if len(robots)>2:
		robotjk = random.sample(robots,2)
		#print(robotjk)
		if(robotjk[0][0]!=robotjk[1][0]):
			#print(robots)
			#print(robotjk[0][0])
			xj,yj,angle,magnitude=update_pairwisedistance(robotjk[0][1],robotjk[0][2],rho_k[robotjk[0][0]-1],robotjk[1][1],robotjk[1][2],rho_k[robotjk[1][0]-1],times,mu)
			#send this xj yj to robot j

			message=str(robotjk[0][0])+' '+str(xj)+' '+str(yj)+' '+str(magnitude)+' '+str(angle)
			#print(message)
			sender.send(message.encode('utf-8'))
			#print(message)
			#time.sleep(magnitude)
	#return robots

robot = Robot()
timestep =32

sender = robot.getEmitter('emitter')
receiver = robot.getReceiver('receiver')
receiver.enable(timestep)

rho_bar, sigma =10,100
mu=100
l=5*rho_bar
times=pow(2,-8)

rho_k = normal_distribution(rho_bar,sigma,N)
print(rho_k)
RSSI_strings=np.empty(4, dtype='object')
RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""

node_ids=np.zeros(N,dtype=int)
rssis=np.ones(N,dtype=float)
arrays=rfn.merge_arrays((node_ids,rssis))
ref_node1 = arrays.copy()
ref_node2 = arrays.copy()
ref_node3= arrays.copy()
ref_node4= arrays.copy()

while robot.step(timestep) != -1:
	try:
		message_counter=0
		for i in range(4):
			if receiver.getQueueLength() > 0:
				message = receiver.getData().decode('utf-8')
				#print(message)
				if message.find("ref-node1:",0,10) !=-1:
					# message.rstrip('\x00')
					RSSI_strings[0]= message.split(" ",-1)
					# if RSSI_strings[0].count('\x00') > 0:
						# RSSI_strings[0].remove('\x00')
					del RSSI_strings[0][0]
					message_counter+=1
				if message.find("ref-node2:",0,10) !=-1:
					# message.rstrip('\x00')
					RSSI_strings[1]=  message.split(" ",-1)
					# if RSSI_strings[1].count('\x00') > 0:
						# RSSI_strings[1].remove('\x00')
					del RSSI_strings[1][0]
					message_counter+=1
				if message.find("ref-node3:",0,10) !=-1:
					# message.rstrip('\x00')
					RSSI_strings[2]=  message.split(" ",-1)
					# if RSSI_strings[2].count('\x00') > 0:
						# RSSI_strings[2].remove('\x00')
					del RSSI_strings[2][0]
					message_counter+=1
				if message.find("ref-node4:",0,10) !=-1:
					# message.rstrip('\x00')
					RSSI_strings[3]=  message.split(" ",-1)
					# if RSSI_strings[3].count('\x00') > 0:
						# RSSI_strings[3].remove('\x00')
					del RSSI_strings[3][0]
					message_counter+=1
				receiver.nextPacket()
	except:
		print("decode error")
	print(RSSI_strings)
	if len(RSSI_strings[0]) ==N:
		# try:
		for x in range(RSSI_strings.size):
			for y in range(len(RSSI_strings[x])):
				if(x==0):
					RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
					RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
					RSSI_strings[x][y][0]=int(RSSI_strings[x][y][0]) #covert robot id string to int
					ref_node1[RSSI_strings[x][y][0]-1][0]=RSSI_strings[x][y][0]
					ref_node1[RSSI_strings[x][y][0]-1][1]=RSSI_strings[x][y][1]
					# print(RSSI_strings[x][y])
				if(x==1):
					RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
					RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
					RSSI_strings[x][y][0]=int(RSSI_strings[x][y][0]) #covert robot id string to int
					ref_node2[RSSI_strings[x][y][0]-1][0]=RSSI_strings[x][y][0]
					ref_node2[RSSI_strings[x][y][0]-1][1]=RSSI_strings[x][y][1]
					# print(RSSI_strings[x][y])
				if(x==2):
					RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
					RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
					RSSI_strings[x][y][0]=int(RSSI_strings[x][y][0]) #covert robot id string to int
					ref_node3[RSSI_strings[x][y][0]-1][0]=RSSI_strings[x][y][0]
					ref_node3[RSSI_strings[x][y][0]-1][1]=RSSI_strings[x][y][1]
					# print(RSSI_strings[x][y])
				if(x==3):
					RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
					RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
					RSSI_strings[x][y][0]=int(RSSI_strings[x][y][0]) #covert robot id string to int
					ref_node4[RSSI_strings[x][y][0]-1][0]=RSSI_strings[x][y][0]
					ref_node4[RSSI_strings[x][y][0]-1][1]=RSSI_strings[x][y][1]


		# except:
			# print("string convertion error")
		refnonzero1=0
		refnonzero2=0
		refnonzero3=0
		refnonzero4=0
		for n in range(N):
			refnonzero1=refnonzero1+ np.count_nonzero(ref_node1[n][0])
			refnonzero2=refnonzero2+ np.count_nonzero(ref_node2[n][0])
			refnonzero3=refnonzero3+ np.count_nonzero(ref_node3[n][0])
			refnonzero4=refnonzero4+ np.count_nonzero(ref_node4[n][0])
		# print(refnonzero1)
		# print(refnonzero2)
		# print(refnonzero3)
		# print(refnonzero4)
		if refnonzero1==N and refnonzero2==N and refnonzero3==N and refnonzero4==N:
			# print(ref_node1)
			# print("test1")
			# print(ref_node2)
			# print("test2")
			# print(ref_node3)
			# print("Test3")
			# print(ref_node4)
			# print("test4")
			for i in range(10):
				del RSSI_strings[0][len(RSSI_strings[0])-1]
				del RSSI_strings[1][len(RSSI_strings[1])-1]
				del RSSI_strings[2][len(RSSI_strings[2])-1]
				del RSSI_strings[3][len(RSSI_strings[3])-1]
			message_counter=0
			RSSI_strings=np.empty(4, dtype='object')
			RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""
			localize_robots(ref_node1,ref_node2,ref_node3,ref_node4)

			node_ids=np.zeros(N,dtype=int)
			rssis=np.ones(N,dtype=float)
			arrays=rfn.merge_arrays((node_ids,rssis))
			ref_node1 = arrays.copy()
			ref_node2 = arrays.copy()
			ref_node3= arrays.copy()
			ref_node4= arrays.copy()
		else:
			#print("incomplete")
			RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""
			RSSI_strings=np.empty(4, dtype='object')
