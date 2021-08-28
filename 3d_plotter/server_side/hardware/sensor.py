import RPi.GPIO as gpio


class Sensor:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(pin, gpio.IN)
    
    def detect(self):
        if gpio.input(self.pin) == 1:
            return True