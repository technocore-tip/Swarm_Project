from controller import Robot
from controller import Receiver
import time
import numpy as np         
from itertools import combinations
import q
from pairwise_actions import distance_vector,distance_magnitude,update_pairwisedistance
def normal_distribution(mu,sigma,N):
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

def localize_robots(RSSI_strings):
	ref_node=np.array([[2,2],[-2,2],[-2,-2],[2,-2]])
	robots= list()
	robots.clear()
	for x in range(RSSI_strings.size):
		for y in range(len(RSSI_strings[x])):
			RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
			RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
			RSSI_strings[x][y][0]=int(RSSI_strings[x][y][0]) #covert robot id string to int
	for n in range(len(RSSI_strings[0])):
		X=np.array([[2*(ref_node[0][0]-ref_node[3][0]),2*(ref_node[0][1]-ref_node[3][1])],
				[2*(ref_node[1][0]-ref_node[3][0]),2*(ref_node[1][1]-ref_node[3][1])],
				[2*(ref_node[2][0]-ref_node[3][0]),2*(ref_node[2][1]-ref_node[3][1])]])
		a=np.array([
		[(pow(ref_node[0][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[0][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/RSSI_strings[0][n][1]),2)+pow(np.sqrt(1/RSSI_strings[3][n][1]),2))],
		[(pow(ref_node[1][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[1][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/RSSI_strings[1][n][1]),2)+pow(np.sqrt(1/RSSI_strings[3][n][1]),2))],
		[(pow(ref_node[2][0],2)-pow(ref_node[3][0],2))+(pow(ref_node[2][1],2)-pow(ref_node[3][1],2)-pow(np.sqrt(1/RSSI_strings[2][n][1]),2)+pow(np.sqrt(1/RSSI_strings[3][n][1]),2))]])
		xy=a/X
		x,y=xy[2][0],xy[0][1]
		robots.append([RSSI_strings[0][n][0],x,y])
		#print("Real-Time Location (m):node=",n,"x=",x,"y=",y)
		#print(robots)
		if len(robots)>2:
			robotjk = random.sample(robots,2)
			#print(robotjk)
			xj,yj=update_pairwisedistance(robotjk[0][1],robotjk[0][2],rho_k[robotjk[0][0]-1],robotjk[1][1],robotjk[1][2],rho_k[robotjk[1][0]-1],times,mu)
			#send this xj yj to robot j 
			print("xj =",xj,"yj",yj)
	RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""
	
	#return robots

robot = Robot()
timestep =32

receiver = robot.getReceiver('receiver')
receiver.enable(timestep)

N=1
rho_bar, sigma =0, 100
mu=100
l=5*rho_bar
times=pow(2,-8)

rho_k = normal_distribution(rho_bar,sigma,N)

message_counter=0
RSSI_strings=np.empty(4, dtype='object')
RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""

# while robot.step(timestep) != -1:	 
	# if receiver.getQueueLength() > 0: 
		# message = receiver.getData().decode('utf-8')
		# if message.find("ref-node1:",0,10) !=-1:
			# message.rstrip('\x00')
			# RSSI_strings[0]= message.split(" ",-1)
			# if RSSI_strings[0].count('\x00') > 0:
				# RSSI_strings[0].remove('\x00')
			# del RSSI_strings[0][0]
			# message_counter+=1
		# if message.find("ref-node2:",0,10) !=-1:
			# message.rstrip('\x00')
			# RSSI_strings[1]=  message.split(" ",-1)
			# if RSSI_strings[1].count('\x00') > 0:
				# RSSI_strings[1].remove('\x00')
			# del RSSI_strings[1][0]
			# message_counter+=1
		# if message.find("ref-node3:",0,10) !=-1:
			# message.rstrip('\x00')
			# RSSI_strings[2]=  message.split(" ",-1)
			# if RSSI_strings[2].count('\x00') > 0:
				# RSSI_strings[2].remove('\x00')
			# del RSSI_strings[2][0]
			# message_counter+=1
		# if message.find("ref-node4:",0,10) !=-1:
			# message.rstrip('\x00')
			# RSSI_strings[3]=  message.split(" ",-1)
			# if RSSI_strings[3].count('\x00') > 0:
				# RSSI_strings[3].remove('\x00')
			# del RSSI_strings[3][0]
			# message_counter+=1
		# receiver.nextPacket()
		
	# if len(RSSI_strings[0]) > 1:
		# for i in range(N):
			# del RSSI_strings[0][len(RSSI_strings[0])-1]
			# del RSSI_strings[1][len(RSSI_strings[1])-1]
			# del RSSI_strings[2][len(RSSI_strings[2])-1]
			# del RSSI_strings[3][len(RSSI_strings[3])-1]
		# message_counter=0
		print(RSSI_strings)
		# localize_robots(RSSI_strings)