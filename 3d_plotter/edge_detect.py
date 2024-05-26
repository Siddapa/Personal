import cv2 as cv
import keyboard

class EdgeDetect:
    def __init__(self, img):
        self.img = img
        self.canny_img = None
        self.contours = None

    """
    Resizes image to work with dimensions of 3D plotter's bed
    Width is mandated to 800 pixels and height is scaled
    proportionally to retain aspect ratio
    """
    def adjust_image(self, blur_size):
        self.width = 800
        scale_ratio = self.img.shape[1] / self.width
        self.height = int(self.img.shape[0] / scale_ratio)

        resize = cv.resize(self.img, (self.width, self.height))
        blur = cv.blur(resize, blur_size)

        self.img = blur
    
    """
    Adjusts thresholds for the Canny filter manually
    Lower threshold: d increases, a decreases
    Upper threshold: l increases, j decreases
    """
    def save_canny_img(self, lower_thresh, upper_thresh):
        self.canny_img = cv.Canny(self.img, int(lower_thresh), int(upper_thresh))
        cv.imwrite("static/__canny_temp.png", self.canny_img)


    def find_contours(self):
        self.contours, _ = cv.findContours(self.canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
