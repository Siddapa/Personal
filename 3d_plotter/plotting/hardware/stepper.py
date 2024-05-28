from time import sleep
import keyboard
import RPi.GPIO as gpio
from .sensor import Sensor

"""
Handles movement for the left-to-right stepper motor
Adjusted by the frequency of on-off pulses from the GPIO
Range of 1400 ticks with 1 being left and 0 being right
"""
class XStepper:
    def __init__(self):
        self.step_pin = 6
        self.dir_pin = 13
        self.sensor_pin = 16

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.x_sens = Sensor(self.sensor_pin)

        self.pos = 0
        self.target_pos = 0
        self.max_steps = 0
        self.base_delay = 0.002
        self.direction = 0
    
    def calibrate(self):
        # self.move(100, 0)
        self.pos = 0
    
    def move(self, steps, direction):
        if direction == 1:
            gpio.output(self.dir_pin, 1)
        elif direction == -1:
            gpio.output(self.dir_pin, 0)
        self.direction = direction
        self.target_pos = steps

    def update(self, ret_queue):
        while self.pos != self.target_pos:
            gpio.output(self.step_pin, 1)
            sleep(self.base_delay)
            gpio.output(self.step_pin, 0)
            sleep(self.base_delay)
            
            self.pos += self.direction
            # print('X', self.pos)
        ret_queue.put(self)


"""
Handles movement for the front-to-back stepper motor
Adjusted by the frequency of on-off pulses from the GPIO
Range of _ ticks with 1 towards the front and 0 towards the back
"""
class YStepper:
    def __init__(self):
        self.step_pin = 19
        self.dir_pin = 26
        self.sensor_pin = 21

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.y_sens = Sensor(self.sensor_pin)

        self.pos = 0
        self.max_steps = 0
        self.base_delay = 0.002
        self.target_pos = 0
        self.target_delay = 0
        self.direction = 0
    
    def calibrate(self):
        self.pos = 0

    def move(self, steps, direction, delay):
        # 0 is back, 1 is forward
        if direction == -1:
            gpio.output(self.dir_pin, 0)
        elif direction == 1:
            gpio.output(self.dir_pin, 1)
        self.target_pos = steps
        self.target_delay = delay
        self.direction = direction
    
    """
    Moves the designated distance set by move()
    Returns true if target reached
    """
    def update(self, ret_queue):
        while self.pos != self.target_pos:
            gpio.output(self.step_pin, 1)
            sleep(self.target_delay)
            gpio.output(self.step_pin, 0)
            sleep(self.target_delay)

            self.pos += self.direction
        ret_queue.put(self)


"""
Handles movement for the up-and-down stepper motor
Positions are binary where the pen is off or on the paper,
no variation in between
1 is down, 0 is up
"""
class ZStepper:
    def __init__(self):
        self.step_pin = 0
        self.dir_pin = 5
        self.sensor_pin = 20
        self.lifted = False

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)
        self.z_sens = Sensor(self.sensor_pin)
        
        self.step_change = 40
        self.base_delay = 0.01
    

    def calibrate(self):
        self.pos = 0
        self.lifted = False


    def lift_pen(self):
        gpio.output(self.dir_pin, 0)
        self.move(self.step_change, self.base_delay)
        self.lifted = True

    def drop_pen(self):
        gpio.output(self.dir_pin, 1)
        self.move(self.step_change, self.base_delay)
        self.lifted = False
    
    def move(self, steps, delay):
        # 0 is up, 1 is down
        for i in range(steps):
            gpio.output(self.step_pin, 1)
            sleep(delay)
            gpio.output(self.step_pin, 0)
            sleep(delay)
