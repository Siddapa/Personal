import cv2 as cv
import numpy as np
from time import sleep


vid = cv.VideoCapture(0)
while vid.isOpened():
    ret, frame = vid.read()

    if ret == True:
        blur = cv.blur(frame, (5,5))

        lower_range = np.array([60, 36, 30])
        upper_range = np.array([150, 100, 71])
        binary = cv.inRange(blur, lower_range, upper_range)
 
        contours, _ = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        drawn = cv.drawContours(frame, contours, -1, (0, 255, 0), 2)
        cv.imshow('Drawn', drawn)
        cv.waitKey()
    else:
        break

    sleep(0.1)

vid.release()
cv.destroyAllWindows()