import sys
import RPi.GPIO as g


g.setmode(g.BCM)
pin = int(sys.argv[1])
g.setup(pin, g.OUT)
g.output(pin, False)
