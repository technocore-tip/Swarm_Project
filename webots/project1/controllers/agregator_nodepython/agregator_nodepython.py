from controller import Robot
from controller import Receiver
import numpy as np         

robot = Robot()
timestep =10

receiver = robot.getReceiver('receiver')
receiver.enable(timestep)


message_counter=0
RSSI_strings=np.empty(4, dtype='object')
RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""
while robot.step(timestep) != -1:	 
	if receiver.getQueueLength() > 0:
		message = receiver.getData().decode('utf-8')
		if message.find("ref-node1:",0,10) !=-1:
			message.rstrip('\x00')
			RSSI_strings[0]= message.split(" ",-1)
			if RSSI_strings[0].count('\x00') > 0:
				RSSI_strings[0].remove('\x00')
		#	del RSSI_strings[0][len(RSSI_strings[0])-1]
			message_counter+=1
		if message.find("ref-node2:",0,10) !=-1:
			message.rstrip('\x00')
			RSSI_strings[1]=  message.split(" ",-1)
			if RSSI_strings[1].count('\x00') > 0:
				RSSI_strings[1].remove('\x00')
			#del RSSI_strings[1][len(RSSI_strings[0])-1]
			message_counter+=1
		if message.find("ref-node3:",0,10) !=-1:
			message.rstrip('\x00')
			RSSI_strings[2]=  message.split(" ",-1)
			if RSSI_strings[2].count('\x00') > 0:
				RSSI_strings[2].remove('\x00')
			#del RSSI_strings[2][len(RSSI_strings[0])-1]
			message_counter+=1
		if message.find("ref-node4:",0,10) !=-1:
			message.rstrip('\x00')
			RSSI_strings[3]=  message.split(" ",-1)
			if RSSI_strings[3].count('\x00') > 0:
				RSSI_strings[3].remove('\x00')
			#del RSSI_strings[3][len(RSSI_strings[0])-1]
			message_counter+=1
		receiver.nextPacket()
	# print("DONE")
	#print(RSSI_strings[0])
	# print(len(RSSI_strings[0]))
	if len(RSSI_strings[0]) > 1:
		del RSSI_strings[0][len(RSSI_strings[0])-1]
		del RSSI_strings[1][len(RSSI_strings[1])-1]
		del RSSI_strings[2][len(RSSI_strings[2])-1]
		del RSSI_strings[3][len(RSSI_strings[3])-1]
		message_counter=0
		# print(RSSI_strings)
		for x in range(RSSI_strings.size):
			for y in range(len(RSSI_strings[x])):
				RSSI_strings[x][y]=RSSI_strings[x][y].split("_",-1) #split the RSSI values from their respective node no.
				RSSI_strings[x][y][1]=float(RSSI_strings[x][y][1]) #convert string to float
		ref_node=np.array([[2,2],[-2,2],[-2,-2],[2,-2]])
		
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

			print("Real-Time Location (m):node=",n,"x=",x,"y=",y)
		RSSI_strings[0]=RSSI_strings[1]=RSSI_strings[2]=RSSI_strings[3]=""