from time import sleep
import keyboard
import RPi.GPIO as gpio

from .sensor import Sensor

"""
Handles movement for the left-to-right stepper motor
Adjusted by the frequency of on-off pulses from the GPIO
"""
class XStepper:
    def __init__(self):
        self.step_pin = 6
        self.dir_pin = 13
        self.sensor_pin = 16

        gpio.setmode(gpio.BCM)
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.x_sens = Sensor(self.sensor_pin)

        self.pos = 0
        self.max_steps = 0
        self.base_delay = 0.01
    
    def calibrate(self):
        gpio.output(self.dir_pin, 0) # 0 is left, 1 is Right
        while not self.x_sens.detect():
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay)
        self.pos = 0
        print('X Axis Calibrated')
    
    def move(self, steps, dir):
        if dir == 1:
            gpio.output(self.dir_pin, 1)
        elif dir == -1:
            gpio.output(self.dir_pin, 0)

        for i in range(steps):
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay)

"""
Handles movement for the front-to-back stepper motor
Adjusted by the frequency of on-off pulses from the GPIO
"""
class YStepper:
    def __init__(self):
        self.step_pin = 19
        self.dir_pin = 26
        self.sensor_pin = 21

        gpio.setmode(gpio.BCM)
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.y_sens = Sensor(self.sensor_pin)

        self.pos = 0
        self.max_steps = 0
        self.base_delay = 0.005
    
    def calibrate(self):
        gpio.output(self.dir_pin, 1) # 0 is back, 1 is forward
        while not self.y_sens.detect():
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay * 4)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay * 4)
        self.pos = 0
        print('Y Axis Calibrated')

    def move(self, steps, delay):
        if dir == 1:
            gpio.output(self.dir_pin, 0)
        elif dir == -1:
            gpio.output(self.dir_pin, 1)

        for i in range(steps):
            gpio.output(self.step_pin, 1)
            sleep(delay)
            gpio.output(self.step_pin, 0)
            sleep(delay)

"""
Handles movement for the up-and-down stepper motor
Positions are binary where the pen is off or on the paper,
no variation in between
"""
class ZStepper:
    def __init__(self):
        self.step_pin = 0
        self.dir_pin = 5
        self.sensor_pin = 20
        self.lifted = False

        gpio.setmode(gpio.BCM)
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.z_sens = Sensor(self.sensor_pin)
        
        self.step_change = 5
        self.base_delay = 0.01
    
    """
    Slides down until pen passes the photogate
    """
    def calibrate(self):
        gpio.output(self.dir_pin, 1) # 0 is up, 1 is down
        while not self.z_sens.detect():
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay)
        self.pos = 0
        print('Z Axis Calibrated')


    def lift_pen(self):
        gpio.output(self.dir_pin, 0)
        self.move(self.step_change, self.base_delay)
        self.lifted = True

    def drop_pen(self):
        gpio.output(self.dir_pin, 1)
        self.move(self.step_change, self.base_delay)
        self.lifted = False
    
    def move(self, steps, delay):
        for i in range(steps):
            gpio.output(self.step_pin, 1)
            sleep(delay)
            gpio.output(self.step_pin, 0)
            sleep(delay)
