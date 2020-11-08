# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 23:30:01 2020

@author: Paul Vincent Nonat
"""

from controller import Supervisor
from controller import Receiver, Emitter
import time
import csv
import pandas as pd
import numpy as np
from itertools import combinations
import struct
import random
from pairwise_actions import distance_vector,distance_magnitude,calculate_angle
from numpy.lib import recfunctions as rfn

class Driver (Supervisor):
	timeStep = 32
	
	def __init__(self):
		super(Driver, self).__init__()
		self.emitter = self.getEmitter('emitter')
		self.keyboard.enable(Driver.timeStep)
		self.keyboard = self.getKeyboard()

	def run(self):
		robot_list=list()
		translational_field_list=list()
		N=100
#		for x in range(N):
#			robot_list.append(self.getFromDef('R'+str(x+1)))
#		for y in range(N):
#			translational_field_list.append(robot_list[y].getField('translation'))
		previous_message = ''
		trial='WEBOTS-SOL3-T1'
		trial_no=trial
		df_init=pd.read_csv(trial+'.csv')
		x_init=df_init['x'].values.astype('float64')
		y_init=df_init['y'].values.astype('float64')
		rho=df_init['rho'].values.astype('float64')

		tts=231
		combination = (N*(N-1))/2
		print("Initialize")
		message="complete 1"
		while True:
			print("TEST")
			for q in range(tts):
				for w in range(int(combination)):
					print("Running step-"+str(q)+"Interaction-"+str(w))
					nextstep_diff=pd.read_csv(trial_no+'/'+trial_no+'-Step-'+str(q)+'-Interaction-'+str(w)+'.csv')
					nextstep_x=nextstep_diff['x'].values.astype('float64')
					nextstep_y=nextstep_diff['y'].values.astype('float64')
					#for x in range(len(rho)):
					#	nextstep_x[x]=nextstep_x[x]-512

					#print(nextstep_x)
					for j in range(len(rho)):
						#print("Previous Pos- X:"+str(x_init[j])+"Y:"+str(y_init[j])+"Next- X:"+str(nextstep_x[j])+"Y:"+str(nextstep_y[j]))
						xj,yj=distance_vector(x_init[j],y_init[j],nextstep_x[j],nextstep_y[j])
						#print("distance vector- Xj:"+str(xj)+"Yj:"+str(yj))
						magnitude=distance_magnitude(xj,yj)
						angle=calculate_angle(xj,yj)
						#print("computed magnitude"+str(magnitude)+"robot-"+str(j))
						if magnitude >0:
							robot= self.getFromDef('R'+str(j+1))
							robot.translationField = robot.getField('translation')
							message=str(j+1)+' '+str(magnitude)+' '+str(angle) #[0]robot_number, [1]magnitude [2]angle
							#sender.send(message.encode('utf-8'))
							print(message)
							current_pos= robot.translationField.getSFVec3f()
							robot.translationField.setSFVec3f([current_pos[0]+(yj/100),0,current_pos[2]+(xj/100)]) #y,z,x							
							#done=0
							#print("timestep-"+str(q)+"interaction-"+str(w))
							#movement=  (magnitude*10)/128.78
							#print("magnitude"+str(movement))
							self.step(32)
		#					while done!=1:
		#						print("timestep-"+str(q)+"interaction-"+str(w))
		#						try:
		#							if receiver.getQueueLength() > 0:
		#								receive_message = receiver.getData().decode('utf-8')
		#
		#								if receive_message.find("complete",0,9) !=-1:
		#									if(int(message.split(" ",-1)[1]))==j+1:
		#										done=1
		#								receiver.nextPacket()
		#						except:
		#							print("empty command")
		#						robot.step(timestep)
					x_init = nextstep_x
					y_init = nextstep_y

controller= Driver()
controller.run()