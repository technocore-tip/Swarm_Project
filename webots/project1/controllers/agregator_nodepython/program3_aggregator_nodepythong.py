# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 23:30:01 2020

@author: Paul Vincent Nonat
"""

from controller import Robot
from controller import Receiver, Emitter
import time
import csv
import pandas as pd
import numpy as np
from itertools import combinations
import struct
import random
from pairwise_actions import distance_vector,distance_magnitude
from numpy.lib import recfunctions as rfn
N=100

robot = Robot()
timestep =32

sender = robot.getEmitter('emitter')
receiver = robot.getReceiver('receiver')
receiver.enable(timestep)

trial='WEBOTS-SOL3-T1'

df_init=pd.read_csv(trial+'.csv')
x_init=df_init['x'].values.astype('float64')
y_init=df_init['x'].values.astype('float64')
rho=df_init['rho'].values.astype('float64')

timestep=333
combination = (N*(N-1))/2

message="complete 1"
while robot.step(timestep) !=-1 or stopper!=1:
	
	for q in range(timestep):
		for w in range(len(combination)):
			print("Running step-"+str(q)+"Interaction-"+str(w))
			nextstep_diff=pd.read_csv(trial_no+'/'+trial_no+'-Step-'+str(q)+'-Interaction-'+str(w)+'.csv')
			nextstep_x=nextstep_diff['x'].values.astype('float64')
			nextstep_y=nextstep_diff['y'].values.astype('float64')
			
			for j in range(len(rho))
				xj,yj=distance_vector(x_init[j],y_init[j],nextstep_x[j],nextstep_y[j])
				magnitude=distance_magnitude(xj,yj)
				angle=calculate_angle(xj,yj)

				message=str(j+1)+' '+str(magnitude)+' '+str(angle) #[0]robot_number, [1]magnitude [2]angle
				sender.send(message.encode('utf-8'))
				
				done=0
				while done!=1:
					try:
						if receiver.getQueueLength() > 0:
							receive_message = receiver.getData().decode('utf-8')
							
							if receive_message.find("complete",0,9) !=-1:
								if(int(message.split(" ",-1)[1]))==j+1:
									done=1
							receiver.nextPacket()
					except:
						print("empty command")
						
			x_init = nextstep_x
			y_init = nextstep_y
