import cv2 as cv
from edge_detect import EdgeDetect
from plotter import Plotter

working_img = cv.imread('3d_plotter/working_img/triangle.png')
detector = EdgeDetect(working_img)
detector.adjust_image((5, 5))
detector.find_canny_thresh()
canny_img = detector.img
print(detector.contours)
cv.imwrite('3d_plotter/final_img/canny.png', canny_img)

plotter = Plotter(detector.contours)
plotter.draw_image()