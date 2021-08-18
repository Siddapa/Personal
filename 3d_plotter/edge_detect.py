import cv2 as cv
import keyboard

img = cv.imread('img.png')

width = 720
scale_ratio = img.shape[1] / width
height = int(img.shape[0] / scale_ratio)
print(width, height)
resize = cv.resize(img, (width, height))

gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
blur = cv.blur(gray, (5, 5))

lower_thresh = 100
upper_thresh = 200
while 1:
    edge = cv.Canny(blur, lower_thresh, upper_thresh)
    cv.imshow("Image", edge)
    cv.waitKey(0)

    if keyboard.is_pressed('d'):
        lower_thresh += 10
    elif keyboard.is_pressed('a'):
        lower_thresh -= 10

    if keyboard.is_pressed('l'):
        upper_thresh += 10
    elif keyboard.is_pressed('j'):
        upper_thresh -= 10

    del edge
