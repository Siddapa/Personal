import RPi.GPIO as g
from time import sleep


trig = 0

g.setmode(g.BCM)
g.setup(trig, g.OUT)

g.output(trig, True)
sleep(1)
g.output(trig, False)