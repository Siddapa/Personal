import RPi.GPIO as g
from time import sleep


trig = 0

g.setmode(g.BCM)
g.setup(trig, g.OUT)


pwm = g.PWM(trig, 60)
pwm.start(2.5)
sleep(1)
pwm.stop()