from controller import Robot, Motor, Emitter, InertialUnit
import time
import numpy as np
import csv
import pandas as pd
import numpy as np
from itertools import combinations
import struct
import random
from pairwise_actions import distance_vector,distance_magnitude,calculate_angle
from numpy.lib import recfunctions as rfn

import mysql.connector
from mysql.connector import Error

actual_id=0
try:
	connection = mysql.connector.connect(host='localhost',
								 database='nonat',
								 user='nonat',
								 password='password')
	sql_query="INSERT INTO `swarms` (`swarm_id`, `name`) VALUES (NULL, 'a')"
	cursor = connection.cursor()
	cursor.execute(sql_query)
	cursor.execute('select LAST_INSERT_ID()')
	records=cursor.fetchall()
	print(records[0][0])
	actual_id=records[0][0]
	cursor.close()
	connection.close()
except Error as e:
	print("Error connecting to database",e)

node=str(actual_id)+'_'

print("Assigned RobotID: ",node)

TIME_STEP = 32

MAX_SPEED = 6.28

N=100


trial='WEBOTS-SOL3-T1'
trial_no=trial
df_init=pd.read_csv(trial+'.csv')
x_init=df_init['x'].values.astype('float64')
y_init=df_init['y'].values.astype('float64')
rho=df_init['rho'].values.astype('float64')

tts=231
combination = (N*(N-1))/2
print("Initialize")


# create the Robot instance.
robot = Robot()



# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)


emitter = robot.getEmitter('emitter')
receiver = robot.getReceiver('receiver')
receiver.enable(TIME_STEP)

gyros = robot.getInertialUnit('inertial_unit')
gyros.enable(TIME_STEP)

def send_message(message):
	emitter.send(message.encode('utf-8'))

def orientation_angle():
	angle=0
	if(gyros.getRollPitchYaw()[2]<0):
		angle=gyros.getRollPitchYaw()[2]+(2*np.pi)
	else:
		angle=gyros.getRollPitchYaw()[2]
	return angle


def receive_command():
	commands=np.empty(1, dtype='object')
	try:
		if receiver.getQueueLength() > 0:
			message = receiver.getData().decode('utf-8')
			commands = message.split(" ",-1)
			receiver.nextPacket()
	except:
		print("decode error")
		commands.append(0)
		commands.append(0)
		commands.append(0)
		commands.append(0)
		commands.append(0)

	return commands[0],commands[3],commands[4] #node_id,magnitude, angle


def turn_left():
	leftMotor.setVelocity(-MAX_SPEED*0.2)
	rightMotor.setVelocity(MAX_SPEED*0.2)
	robot.step(32)

def turn_right():
	leftMotor.setVelocity(MAX_SPEED*0.2)
	rightMotor.setVelocity(-MAX_SPEED*0.2)
	robot.step(32)

def stop():
	leftMotor.setVelocity(0)
	rightMotor.setVelocity(0)
	robot.step(32)

def rotate(angle):
#	print("rotation ready")
	actual_angle=orientation_angle()
	#print(actual_angle)
	while ((actual_angle> angle+0.2) or (actual_angle < angle-0.2)):
		#print(actual_angle)
		if((actual_angle> angle+0.2) or (actual_angle > angle-0.2)):
			turn_right()
			stop()

		if((actual_angle< angle+0.2) or (actual_angle < angle-0.2)):
			turn_left()
			stop()
		actual_angle=orientation_angle()

def rotate_nofeedback(angle):
	actual_angle=orientation_angle()
	if (actual_angle-angle) >0:
		velocity_percent= (20.5*np.abs(actual_angle-angle))/128.78
		print("turn right")
		leftMotor.setVelocity(MAX_SPEED)
		rightMotor.setVelocity(-(MAX_SPEED))
		robot.step(velocity_percent)
		stop()
	if (actual_angle-angle) <0:
		velocity_percent= (20.5*np.abs(actual_angle-angle))/128.78
		print("turn left")
		leftMotor.setVelocity(-(MAX_SPEED))
		rightMotor.setVelocity(MAX_SPEED)
		robot.step(velocity_percent)
		stop()
		
def move_bot(robot_id,magnitude,angle,actual_id):
	#print("robot id: ",robot_id,"magnitude: ",magnitude,"angle: ",angle,"actual_id: ",actual_id)
	#print(type(robot_id))
	if robot_id == actual_id: #if robotID matches your ID, perform the requested movement, else do nothing
		rotate_nofeedback(angle)
		#print("occured")
		stop()
		movement=  (magnitude*10)/128.78 #1 rotation = 128.78mm, if I need to displace
		print("velocity ratio"+str(movement))
		leftMotor.setVelocity(MAX_SPEED)
		rightMotor.setVelocity(MAX_SPEED)
		robot.step(movement)
		stop()
		robot.step(32)
		#send_message("complete "+str(actual_id))

while robot.step(TIME_STEP) != -1:
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
				if magnitude >0 and (j+1)==actual_id :
					move_bot((j+1),magnitude,angle,actual_id) #do action from command
					robot.step(32)

			x_init = nextstep_x
			y_init = nextstep_y
			
