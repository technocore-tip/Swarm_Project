from controller import Robot, Motor, Emitter, InertialUnit
import time
import numpy as np
import time
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
	robot.step(8)
	
def turn_right():
	leftMotor.setVelocity(MAX_SPEED*0.2)
	rightMotor.setVelocity(-MAX_SPEED*0.2)
	robot.step(8)

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

def move_bot(robot_id,magnitude,angle,actual_id):
	#print("robot id: ",robot_id,"magnitude: ",magnitude,"angle: ",angle,"actual_id: ",actual_id)
	#print(type(robot_id))
	if robot_id == actual_id: #if robotID matches your ID, perform the requested movement, else do nothing
		rotate(angle)
		#print("occured")
		movement=  (6.28*magnitude*10)/128.78 #1 rotation = 128.78mm, if I need to displace 
		leftMotor.setVelocity(movement)
		rightMotor.setVelocity(movement)
		robot.step(TIME_STEP)
		stop()
		send_message("complete "+str(actual_id))
		
while robot.step(TIME_STEP) != -1:
	
	commands=np.empty(1, dtype='object')		
	try:
		if receiver.getQueueLength() > 0:# get command from aggregator node broadcast
			message = receiver.getData().decode('utf-8')
			commands = message.split(" ",-1) #[0]robot_number, [1]magnitude [2]angle
			receiver.nextPacket()
	except:
		print("empty command")
		
	if commands:
		move_bot(int(commands[0]),float(commands[1]),float(commands[2]),actual_id) #do action from command