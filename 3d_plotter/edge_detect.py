import cv2 as cv
import keyboard


"""
Resizes image to work with dimensions of 3D plotter's bed
Width is mandated to 800 pixels and height is scaled
proportionally to retain aspect ratio
"""
def adjust_image(img, blur_size):
    width = 800
    scale_ratio = img.shape[1] / width
    height = int(img.shape[0] / scale_ratio)

    resize = cv.resize(img, (width, height))
    blur = cv.blur(resize, blur_size)

    return blur


"""
Adjusts thresholds for the Canny filter manually
Lower threshold: d increases, a decreases
Upper threshold: l increases, j decreases
"""
def save_canny_img(adjusted_img, lower_thresh, upper_thresh):
    canny_img = cv.Canny(adjusted_img, lower_thresh, upper_thresh)
    cv.imwrite("static/__canny_temp.png", canny_img)


def find_contours(canny_img):
    contours, _ = cv.findContours(canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    return contours
