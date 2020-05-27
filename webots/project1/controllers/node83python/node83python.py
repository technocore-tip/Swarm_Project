from controller import Robot, Motor, Emitter, InertialUnit
import time
import numpy as np
import time
node='83_'
actual_id=83
print("Initializing node",node)
def send_message(message):
	emitter.send(message.encode('utf-8'))
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
	leftMotor.setVelocity(-MAX_SPEED*0.4)
	rightMotor.setVelocity(MAX_SPEED*0.4)
	robot.step(10)
	
def turn_right():
	leftMotor.setVelocity(MAX_SPEED*0.4)
	rightMotor.setVelocity(-MAX_SPEED*0.4)
	robot.step(10)

def stop():
	leftMotor.setVelocity(0)
	rightMotor.setVelocity(0)
	robot.step(10)

def rotate(angle):
#	print("rotation ready")
	actual_angle=orientation_angle()
	#print(actual_angle) 
	while ((actual_angle> angle+0.2) or (actual_angle < angle-0.2)):
		#print(actual_angle)
		send_message(node)
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
		leftMotor.setVelocity(6.28*magnitude)
		rightMotor.setVelocity(6.28*magnitude)
		send_message(node)
		robot.step(TIME_STEP)
		stop()
		robot.step(TIME_STEP)
		
		
while robot.step(TIME_STEP) != -1:
	send_message(node) # send ID 
	
	commands=np.empty(1, dtype='object')		
	try:
		if receiver.getQueueLength() > 0:# get command from aggregator node broadcast
			message = receiver.getData().decode('utf-8')
			commands = message.split(" ",-1)
			receiver.nextPacket()
	except:
		print("empty command")
		
	if commands:
		move_bot(int(commands[0]),float(commands[3]),float(commands[4]),actual_id) #do action from command