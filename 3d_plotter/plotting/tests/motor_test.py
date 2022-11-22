import RPi.GPIO as g
from time import sleep

pinouts = {
    'y_dir': 26,
    'y_step': 19,
    'x_dir': 13,
    'x_step': 6,
    'z_dir': 5,
    'z_step': 0
}
SPR = 100
delay = 0.001
axis = 'y'
step_pin = axis + '_step'
dir_pin = axis + '_dir'

g.setmode(g.BCM)
g.setup(pinouts[step_pin], g.OUT)
g.setup(pinouts[dir_pin], g.OUT)

g.output(pinouts[dir_pin], g.HIGH)
for i in range(SPR):
    g.output(pinouts[step_pin], g.HIGH)
    sleep(delay)
    g.output(pinouts[step_pin], g.LOW)
    sleep(delay)

g.cleanup()
