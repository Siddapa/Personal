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
SPR = 200
delay = 0.01

g.setmode(g.BCM)
for pin in pinouts.values():
    g.setup(pin, g.OUT)

for i in range(SPR):
    g.output(pinouts['y_step'], g.HIGH)
    sleep(delay)
    g.output(pinouts['y_step'], g.LOW)
    sleep(delay)

g.output(pinouts['y_dir'], g.LOW)
for i in range(SPR):
    g.output(pinouts['y_step'], g.HIGH)
    sleep(delay)
    g.output(pinouts['y_step'], g.LOW)
    sleep(delay)

g.cleanup()