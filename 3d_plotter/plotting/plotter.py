from threading import Thread
from math import copysign
# import RPi.GPIO as gpio

from plotting.hardware.stepper import XStepper, YStepper, ZStepper


class Plotter:
    def __init__(self, contours):
        self.contours = contours
        self.x_stepper = XStepper()
        self.y_stepper = YStepper()
        self.z_stepper = ZStepper()
    
    def calibrate(self):
        confirmation = Sensor(16) # Touch sensor from x axis
        while not confirmation.detect():
            sleep(0.1)
        self.x_stepper.calibrate()
        self.y_stepper.calibrate()
        self.z_stepper.calibrate()

    """
    Intially raises pen to not draw a line from calibration point to start of image
    Pen stays down during the duration of a contour until next all points are finished
    """
    def draw_image(self):
        if not self.z_stepper.lifted:
            self.z_stepper.lift_pen()
        
        for index, contour in enumerate(self.contours):
            for point in contour:
                print('Contours Completed: ' + index + ' / ' + len(self.contours))
                print('Perecent Completed: ' + int(index/len(self.contours)));
                self.move(point[0]) # Nested list
                if self.z_stepper.lifted:
                    self.z_stepper.drop_pen()
                self.move(point[0]) # Nested list
            self.z_stepper.lift_pen()

    """
    Finds the change in distance between current position and next position
    Adjusts the front-to-back timing delay for smoother curves (needs to be tested)
    """
    def move(self, point):
        print(point)
        x_change = point[0] - self.x_stepper.pos
        y_change = point[1] - self.y_stepper.pos
        slope = y_change / x_change
        y_delay = self.y_stepper.base_delay * abs(slope)
        x_dir = copysign(1, x_change)
        y_dir = copysign(1, y_change)

        self.x_stepper.move(x_change, x_dir)
        self.y_stepper.move(y_change, y_delay, y_dir)

        # x_thread = Thread(target=self.x_stepper.move, args=[x_change, x_dir])
        # y_thread = Thread(target=self.y_stepper.move, args=[y_change, y_delay, y_dir])
        # x_thread.start()
        # y_thread.start()
        # x_thread.join()
        # y_thread.join()
