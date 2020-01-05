from environment import draw_windows,draw_swarm,distance_magnitude,relative_distance
import time
import threading
import math
from random import randint

lock = threading.Lock()

def dynamics_meeting_point(robot,robots):
    #dynamics of the swarm
    x_total,y_total = relative_distance(robot,robots)
    lock.acquire()
    #print('distance of robot ', robot.id, ' ',x_total,' ',y_total)
    print(robot.id)
    lock.release()
    distance = distance_magnitude(x_total,y_total)
    print(distance)
    #print(robot)
    while distance>0.5:
        loc_x = -x_total/40.0
        loc_y = -y_total/40.0
        lock.acquire()
        #print(robot.id,loc_x,loc_y,distance)
        lock.release()
        robot.move(loc_x,loc_y)
        x_total,y_total = relative_distance(robot,robots)
        distance = distance_magnitude(x_total,y_total)
        time.sleep(0.1)

def simulate_meeting_point(robots):
	#run simulation using multithreading
    for robot in robots:
        dynamics_meeting_point(robot,robots)
#        worker = threading.Thread(target=dynamics_meeting_point,args=(robot,robots))
#        print(worker)
#        worker.setDaemon(True)
#        worker.start()



if __name__ == '__main__':
	#main program
	win = draw_windows(1024,768) #draw window with width = 700 and height = 600
	robots = draw_swarm(70,win) #draw 7 swarm in win
	win.getMouse() #blocking call
	simulate_meeting_point(robots) #start simulation meeting point
	win.getMouse()
