import subprocess
import time
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="--N-robots[Number of Robots]")
	parser.add_argument('--N-robots',type=int,default=100,help='Number of Robots')
	args = parser.parse_args()
	N=args.N_robots
	for i in range(N):
		print("Opening",(i+1))
		subprocess.call('start python node1python_v3.py',shell=True)
		time.sleep(0.2)
	
	#subprocess.call('start python webots_robotpos_randomizer.py',shell=True)