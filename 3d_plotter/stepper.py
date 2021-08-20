from time import sleep
import RPi.GPIO as gpio

from sensor import Sensor


class XStepper:
    def __init__(self):
        self.step_pin = 6
        self.dir_pin = 13
        self.sensor_pin = 16
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.x_sens = Sensor(self.sensor_pin)

        self.pos = 0
        self.max_steps = 0
        self.base_delay = 0.02
    
    def calibrate(self):
        gpio.output(self.dir_pin, 0) # 0 is left, 1 is Right
        while not self.x_sens.detect():
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay)
        self.pos = 0 # TODO Account for offset
    
    def move(self, steps):
        for i in range(steps):
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay)


class YStepper:
    def __init__(self):
        self.step_pin = 19
        self.dir_pin = 26
        self.sensor_pin = 21
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.x_sens = Sensor(self.sensor_pin)

        self.pos = 0
        self.max_steps = 0
        self.base_delay = 0.02
    
    def calibrate(self):
        gpio.output(self.dir_pin, 1) # 0 is back, 1 is forward
        while not self.x_sens.detect():
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay * 4)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay * 4)
        self.pos = 0 # TODO Account for offset

    def move(self, steps, delay):
        for i in range(steps):
            gpio.output(self.step_pin, 1)
            sleep(delay)
            gpio.output(self.step_pin, 0)
            sleep(delay)


class ZStepper:
    def __init__(self):
        self.step_pin = 0
        self.dir_pin = 5
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        
        self.pos = 0
        self.base_delay = 0.02
    
    def calibrate(self):
        # 0 is up, 1 is down
        pass

    def lift_pen():
        pass

    def drop_pen():
        pass