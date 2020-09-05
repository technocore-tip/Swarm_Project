# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 23:12:33 2020

@author: Paul Vincent Nonat
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 23:30:01 2020

@author: Paul Vincent Nonat
"""

import time
import csv
import pandas as pd
import numpy as np
from itertools import combinations
import struct
import random
from pairwise_actions import distance_vector,distance_magnitude,update_pairwisedistance
from numpy.lib import recfunctions as rfn
N=100

#robot = Robot()
timestep =32

#sender = robot.getEmitter('emitter')
#receiver = robot.getReceiver('receiver')
#receiver.enable(timestep)
trial='WEBOTS-SOL3-T1'

df_init=pd.read_csv(trial+'.csv')
x=df_init['x'].values.astype('float64')
y=df_init['x'].values.astype('float64')
rho=df_init['rho'].values.astype('float64')
#while robot.step(timestep) !=-1 or stopper!=1:
