import cv2 as cv
import keyboard

class EdgeDetect:
    def __init__(self, img):
        self.img = img

    def adjust_image(self, blur):
        self.width = 720
        scale_ratio = self.img.shape[1] / self.width
        self.height = int(self.img.shape[0] / scale_ratio)

        resize = cv.resize(self.img, (self.width, self.height))
        gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
        blur = cv.blur(gray, blur)

        self.img = blur
    
    def find_canny_thresh(self):
        self.lower_thresh = 0
        self.upper_thresh = 0
        while 1:
            edge = cv.Canny(self.img, self.lower_thresh, self.upper_thresh)
            cv.imshow("Canny Image", edge)
            cv.waitKey(0)

            if keyboard.is_pressed('d'):
                self.lower_thresh += 10
            elif keyboard.is_pressed('a'):
                self.lower_thresh -= 10

            if keyboard.is_pressed('l'):
                self.upper_thresh += 10
            elif keyboard.is_pressed('j'):
                self.upper_thresh -= 10
            
            if keyboard.is_pressed('s'):
                print(self.lower_thresh, self.upper_thresh)
                self.img = edge
                break

            del edge
        self.contours, _ = cv.findContours(self.img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)