from time import sleep
import keyboard
import requests as gpio

from .sensor import Sensor


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
        self.lifted = False
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        
        self.step_change = 5
        self.base_delay = 0.01
    
    def calibrate(self):
        while 1:
            if keyboard.is_pressed('up'):
                g.output(self.dir_pin, 0)
                self.move(1, self.base_delay)
            if keyboard.is_pressed('down'):
                g.output(self.dir_pin, 1)
                self.move(1, self.base_delay)
            if keyboard.is_pressed('enter'):
                self.lifted = False
                break

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