import RPi.GPIO as gpio


"""
Template class one bit digital signal
Commonly used for touch sensors
"""
class Sensor:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(pin, gpio.IN)
    
    def detect(self):
        if gpio.input(self.pin) == 1:
            return True
        return False