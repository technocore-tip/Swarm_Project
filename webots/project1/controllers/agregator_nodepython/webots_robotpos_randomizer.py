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
		N=200
		print("Randomize Robot Position")
		message="complete 3"
		
		#move robot outside the field
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
			robot.translationField.setSFVec3f([random.uniform(-2.1,2.1),0,random.uniform(-2.1,2.1)])#y,z,x
			self.step(8)
controller= Driver()
controller.run()