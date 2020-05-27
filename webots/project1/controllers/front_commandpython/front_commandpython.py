from controller import Robot, Motor, Emitter, InertialUnit
import time
node='1_'
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
emitter = robot.getEmitter('emitter')
gyros = robot.getInertialUnit('inertial_unit')
gyros.enable(TIME_STEP)
# set up the motor speeds at 10% of the MAX_SPEED.
leftMotor.setVelocity(0 * MAX_SPEED)
rightMotor.setVelocity(0 * MAX_SPEED)

while robot.step(TIME_STEP) != -1:
	send_message(node)
	#print(gyros.getRollPitchYaw()[2])