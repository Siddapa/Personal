import numpy as numpy
import cv2 as cv
from time import time

start = time()
img = cv.imread('blah3.jpg')
img = cv.resize(img, (640, 480))
cv.imshow('rings_orig', img)
img = cv.cvtColor(img, cv.COLOR_RGB2HSV)
cv.imshow('rings_hsv', img)

# 17, 235, 148
orange_lower_range = np.array([13, 50, 50])
orange_upper_range = np.array([255, 255, 255])

orange_mask = cv.inRange(img, orange_lower_range, orange_upper_range)
result = cv.bitwise_and(img, img, mask=orange_mask)

result = cv.cvtColor(result, cv.COLOR_HSV2BGR)

top_left = (265, 210)
bottom_right = (279, 215)
low_lum = 60
high_lum = 100

gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
blur = cv.blur(gray, (3, 3))
ret, thresh = cv.threshold(blur, 0, 150, cv.THRESH_BINARY)

contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

#4000 is area for 4 rings
#3000 is are for 1 ring
contour_color = (0, 255, 0)
for index, contour in enumerate(contours):
    area = cv.contourArea(contour)
    if area > 1000:
        cv.drawContours(result, contours, index, contour_color, 1, 8, hierarchy)
        print(area)

stop = time()
print(stop-start)
cv.imshow('rings_masked', result)
cv.waitKey(0)
cv.destroyAllWindows()
