import random

import cv2 as cv
import numpy as np


class Field:
    def __init__(self, FIELD_SIZE, FIELD_COLOR, ROCK_COLOR):
        """
            field : np.array
                FIELD_SIZE array filled with 3, 8-bit pixels
            FIELD_SIZE : tuple
                2 element tuple with length (in px) and width (in px)
            ROCK_COLOR : tuple
                3 element pixel data
        """
        self.FIELD_SIZE = FIELD_SIZE
        self.FIELD_COLOR = FIELD_COLOR
        self.ROCK_COLOR = ROCK_COLOR
        self.field = np.empty(self.FIELD_SIZE, np.uint8)
        self.field.fill(np.array(self.FIELD_COLOR))
        self.generate()


    def update(self):
        # Rock Update
        return None


    def display(self):
        cv.imshow("Field", self.field)
        cv.waitKey()


    def generate(self):
        rock_limit = 1000
        rock_radius = 10 # In pixels

        for i in range(rock_limit):
            center = (random.randint(0, self.FIELD_SIZE[0]-1), random.randint(0, self.FIELD_SIZE[1]-1))
            test_pixel = self.field[center[0], center[1]]
            if np.array_equal(np.array(self.ROCK_COLOR), test_pixel):
                continue

            cv.circle(self.field, center, rock_radius, self.ROCK_COLOR, -1)
        self.display()


class Robot:
    def __init__(self, top_left, top_right, color):
        """
            top_left : tuple
                Two element tuple with coordinates of rectangle (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
            top_right : tuple

        """
        self.COLOR = color
        self.top_left = top_left
        self.bottom_right = top_right


if __name__ == '__main__':
    FIELD_SIZE = (5000, 5000)
    FIELD_COLOR = (0, 200, 0)
    ROCK_COLOR = (200, 200, 200)

    field = Field(FIELD_SIZE, FIELD_COLOR, ROCK_COLOR)
    robot = Robot((0, 0), (20, 20), (0, 255, 0))
