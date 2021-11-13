import socket
import os
import cv2 as cv
import numpy as np


from edge_detect import EdgeDetect


if __name__ == '__main__':
    HOST = '192.168.68.126'
    PORT = 65432
    os.chdir('C:\\Users\\vishn\\Personal\\3d_plotter\\client_side')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        filename = input('Input Filename with Extension: ')
        working_img = cv.imread('working_files/' + filename)

        detector = EdgeDetect(working_img)
        detector.adjust_image((5, 5))
        detector.find_canny_thresh()
        
        cv.imwrite('final_files/canny.png', detector.img)

        with open('final_files/arr', 'wb') as f:
            np.save(f, detector.contours)

        s.sendfile(open('final_files/arr', 'rb'))