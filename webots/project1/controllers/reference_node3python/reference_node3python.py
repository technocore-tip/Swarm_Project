from controller import Robot
from controller import Receiver, Emitter

robot = Robot()
timestep =32
N=200
sender = robot.getEmitter('emitter')
receiver = robot.getReceiver('receiver')
receiver.enable(timestep)
def send_message(message):
	sender.send(message.encode('utf-8'))

def receive_message():
	node_message='ref-node3:'
	for i in range(N):
		temp=''
		if receiver.getQueueLength() > 0:
			try:
				message = receiver.getData().decode('utf-8')
				signal = receiver.getSignalStrength()
				temp=' '+message+str(signal)
				node_message=node_message+temp
				receiver.nextPacket()
			except:
				print("error")
	return node_message
	
	#except:
	#	print("decode error")
while robot.step(timestep) != -1:
	send_readings=receive_message()
	#print(send_readings)
	send_message(send_readings)