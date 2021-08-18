import RPi.GPIO as g

g.setmode(g.BCM)
g.setup(4, g.OUT)

while 1:
	g.output(4, True)
	g.output(4, False)
