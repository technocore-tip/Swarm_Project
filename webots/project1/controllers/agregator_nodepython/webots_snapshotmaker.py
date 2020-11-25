# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 23:30:01 2020

@author: Paul Vincent Nonat
"""
# create a randomize robot position on the webots environment which the user can save as .wbt

from controller import Supervisor
from controller import Receiver, Emitter
import time
import pandas as pd
import numpy as np
from itertools import combinations
import struct
import random
from pairwise_actions import distance_vector,distance_magnitude,calculate_angle
from numpy.lib import recfunctions as rfn
import os


class Driver (Supervisor):
	timeStep = 8
	
	def __init__(self):
		super(Driver, self).__init__()
		self.emitter = self.getEmitter('emitter')
		self.keyboard.enable(Driver.timeStep)
		self.keyboard = self.getKeyboard()

	def run(self):
		robot_list=list()
		translational_field_list=list()
		N=100
		tts=200 #number of timestep
		trial_no="WEBOTS-SOL3-T4"
		path="C:/Users/Paul Vincent Nonat/Documents/Graduate Student Files/agregator_nodepython/"+trial_no+"_snapshot/"
		if not os.path.exists(trial_no+"_snapshot"):
			os.makedirs(trial_no+"_snapshot")
		combination=N*(N-1)/2
		print("Randomize Robot Position")
		message="complete 3"
		
		#move robot outside the field
		#snapshot pos 0
		self.exportImage(path+str(0)+".jpg",100)
		for x in range(tts+1):
			print("timestep",x)
			nextstep_diff=pd.read_csv(trial_no+'/'+trial_no+'-Step-'+str(x)+'-Interaction-'+str(int(combination-1))+'.csv')
			nextstep_x=nextstep_diff['x'].values.astype('float64')
			nextstep_y=nextstep_diff['y'].values.astype('float64')
			
			for j in range(N):

				robot= self.getFromDef('R'+str(j+1))
				robot.translationField = robot.getField('translation')
				print("Transfer"+str(j))
				current_pos= robot.translationField.getSFVec3f()
				robot.translationField.setSFVec3f([current_pos[0]+10,0,current_pos[2]+10]) #y,z,x							
				self.step(8)
		
			for j in range(N):
				robot= self.getFromDef('R'+str(j+1))
				robot.translationField = robot.getField('translation')
				robot.translationField.setSFVec3f([(nextstep_y[j]/100),0,(nextstep_x[j]/100)])#y,z,x
				self.step(8)
			#self.step(32)
			self.exportImage(path+str(x+1)+".jpg",100)
controller= Driver()
controller.run()