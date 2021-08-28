import RPi.GPIO as g
import time

g.setmode(g.BCM)
g.setup(16, g.IN)
g.setup(20, g.IN)
g.setup(21, g.IN)


while 1:
	print(g.input(16))
	print(g.input(20))
	print(g.input(21))
	print()
	time.sleep(1)
