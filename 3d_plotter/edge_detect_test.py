import os
from io import StringIO
import cv2 as cv
from edge_detect import EdgeDetect
import socket
import pickle
import numpy as np


def contour_test():
    os.chdir('C:\\Users\\vishn\\Personal\\3d_plotter\\client_side')
    filename = input('Input Filename with Extension: ')
    working_img = cv.imread('working_files/' + filename)

    detector = EdgeDetect(working_img)
    detector.adjust_image((5, 5))
    detector.find_canny_thresh()


def server_test():
    HOST = ''
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            contours = conn.recv(1000000) # Average file size is around 200 KB
            conn.sendall(b'Received!')
            # contours = np.load(StringIO(contours))['frame']
            # print(contours)
            contours = pickle.loads(contours)

            
            black_image = np.zeros((800, 800, 3), dtype = "uint8")
            for contour in contours:
                for point in contour:
                    x_coord = point[0][0]
                    y_coord = point[0][1]
                    black_image[x_coord, y_coord] = (255, 255, 255)
            cv.imshow('Plot', black_image)
            cv.waitKey(0)


if __name__ == '__main__':
    server_test()