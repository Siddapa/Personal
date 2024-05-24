from multiprocessing import Process, Queue
from math import copysign
from time import sleep
from plotting.hardware.stepper import XStepper, YStepper, ZStepper
from plotting.hardware.sensor import Sensor
from reprint import output


class Plotter:
    def __init__(self, contours):
        self.contours = contours
        self.x_stepper = XStepper()
        self.y_stepper = YStepper()
        self.z_stepper = ZStepper()
    

    def calibrate(self):
        confirmation = Sensor(20) # Touch sensor from z axis
        while not confirmation.detect():
            sleep(0.1)
        self.x_stepper.calibrate()
        self.y_stepper.calibrate()
        self.z_stepper.calibrate()
        print()

    """
    Intially raises pen to not draw a line from calibration point to start of image
    Pen stays down during the duration of a contour until next all points are finished
    """
    def draw_image(self):
        if not self.z_stepper.lifted:
            self.z_stepper.lift_pen()
        
        with output(output_type='dict') as output_lines:
            for index, contour in enumerate(self.contours):
                for point in contour:
                    self.move(point[0]) # Nested list

                    output_lines['Percent Completed'] = f'{str(index/len(self.contours) * 100)}'
                    output_lines['Contours Completed'] = f'{index} / {len(self.contours)}'
                    output_lines['Positions'] = f'X_Pos - {self.x_stepper.pos}, Y_Pos - {self.y_stepper.pos}, X_Target - {self.x_stepper.target_pos}, Y_Target - {self.y_stepper.target_pos}'

                    # percent_completed = f'Percent Completed: {str(int(index/len(self.contours)))}'
                    # contours_completed = f'Contours Completed: {str(index)} / {str(len(self.contours))}'
                    # positions = f'X Pos: {self.x_stepper.pos},  Y Pos: {self.y_stepper.pos}, X Target: {self.x_stepper.target_pos}, Y Target: {self.y_stepper.target_pos}'
                    # print(f'{percent_completed}\n{contours_completed}\n{positions}')
                    
                    ret_queue = Queue()
                    x_process = Process(target=self.x_stepper.update, args=(ret_queue,))
                    y_process = Process(target=self.y_stepper.update, args=(ret_queue,))
                    x_process.start()
                    y_process.start()
                    x_process.join()
                    y_process.join()

                    # Need to check class type of queue objects since we can't guarantee order
                    first = ret_queue.get()
                    if isinstance(first, XStepper):
                        self.x_stepper = first
                        self.y_stepper = ret_queue.get()
                    else:
                        self.y_stepper = first
                        self.x_stepper = ret_queue.get()

                    if self.z_stepper.lifted:
                        self.z_stepper.drop_pen()
                self.z_stepper.lift_pen()


    """
    Finds the change in distance between current position and next position
    Adjusts the front-to-back timing delay for smoother curves
    """
    def move(self, point):
        x_change = point[0] - self.x_stepper.pos
        y_change = point[1] - self.y_stepper.pos
        slope = x_change / y_change if y_change == 0 else 1
        y_delay = self.y_stepper.base_delay * abs(slope)
        x_dir = copysign(1, x_change)
        y_dir = copysign(1, y_change)
        self.x_stepper.move(point[0], x_dir)
        self.y_stepper.move(point[1], y_dir, y_delay)
