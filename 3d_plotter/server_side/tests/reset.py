import RPi.GPIO as g

g.setmode(g.BCM)
g.setup(19, g.OUT)
g.output(19, False)