import subprocess
import time

N=100

for i in range(N):
	print("Opening",(i+1))
	subprocess.call('start python program3_slave.py',shell=True)
	time.sleep(0.2)
