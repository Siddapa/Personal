import RPi.GPIO as g
from time import sleep

g.setmode(g.BCM)
g.setup(16, g.IN)
g.setup(20, g.IN)
g.setup(21, g.IN)


while 1:
    print(g.input(16), g.input(20), g.input(21), end='\r')
    sleep(0.1)
