import numpy as np
import cv2 as cv
from time import time

def getCornersFromPoints(points):
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0

    for point in points:
        x = point[0][0]
        y = point[0][1]

        if (minX == 0 or x < minX):
            minX = x
        if (minY == 0 or y < minY):
            minY = y
        if (maxX == 0 or x > maxX):
            maxX = x
        if (maxY == 0 or y > maxY):
            maxY = y

    corners = [(minX, minY), (minX, maxY), (maxX, minY), (maxX, maxY)]
    return corners

start = time()
img = cv.imread('C:\\Users\\vishn\\Documents\\Personal\\FTC\\Auto_Aim_Images\\blah.jpg')
resized = cv.resize(img, (800, 448))
bgr = cv.cvtColor(resized, cv.COLOR_RGBA2BGR)
hls = cv.cvtColor(bgr, cv.COLOR_BGR2HLS)
blurred = cv.blur(hls, (1, 1))

# 17, 235, 148
lower_range = np.array([0, 50, 150])
upper_range = np.array([20, 100, 255])
binary = cv.inRange(blurred, lower_range, upper_range)
contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

maxArea = -1
maxContourIndex = -1
for index, contour in enumerate(contours):
    area = cv.contourArea(contour)
    if area > maxArea:
        maxContourIndex = index
        maxArea = area
contoured = cv.drawContours(resized, contours, maxContourIndex, (0, 255, 0), 2)

biggest = contours[maxContourIndex]
corners = getCornersFromPoints(biggest)
x_center = (corners[0][0]+corners[3][0])/2
pixel_turn = 400 - x_center
print(pixel_turn)

end = time()
cv.imshow('Final', contoured)
cv.imwrite('Contoured.jpg', contoured)


cv.waitKey()
cv.destroyAllWindows()
