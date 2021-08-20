from threading import Thread
import RPi.GPIO as gpio

from stepper import XStepper, YStepper, ZStepper


class Plotter:
    def __init__(self, contours):
        self.contours = contours
        self.x_stepper = XStepper()
        self.y_stepper = YStepper()
        self.z_stepper = ZStepper()
        gpio.setmode(gpio.BCM)
    
    def draw_image(self):
        for contour in self.contours:
            for point in contour:
                self.z_stepper.lift_pen()
                self.move(point[0]) # Nested list
                self.drop_pen()
                self.move(point[0]) # Nested list

    def move(self, point):
        x_change = point[0] - self.x_stepper.pos
        y_change = point[1] - self.y_stepper.pos
        slope = y_change / x_change
        y_delay = self.y_stepper.base_delay * slope

        x_thread = Thread(target=self.x_stepper.move, args=[x_change])
        y_thread = Thread(target=self.y_stepper.move, args=[y_change, y_delay])
        x_thread.start()
        y_thread.start()
        x_thread.join()
        y_thread.join()