import socket
import pickle
import numpy as np
import cv2 as cv
from edge_detect import EdgeDetect
# from plotting.plotter import Plotter


class Server:
    def __init__(self, address, port) -> None:
        self.address = address
        self.port = port
        self.packet_size = 10000000

    def await_receive(self) -> None:
        tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tunnel.bind((self.address, self.port))
        tunnel.listen()
        conn, _ = tunnel.accept()
        data = conn.recv(self.packet_size)
        self.contours = pickle.loads(data)
    

    # def draw(self) -> None:
    #     plotter = Plotter(self.contours) 
    #     plotter.calibrate()
    #     plotter.draw_image()

    
    def display_contours(self) -> None:
        black_image = np.zeros((800, 800, 3), dtype = "uint8")
        for contour in self.contours:
            for point in contour:
                x_coord = point[0][0]
                y_coord = point[0][1]
                black_image[y_coord, x_coord] = [0, 255, 0]
        cv.imshow('Plot', black_image)
        cv.waitKey(0)


class Client:
    def __init__(self, address, port) -> None:
        self.address = address
        self.port = port

    def send(self) -> None:
        tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tunnel.connect((self.address, self.port))
        contours = self.detect_image()

        data = pickle.dumps(contours)
        tunnel.send(data)
    
    def detect_image(self):
        filename = input('Input Filename with Extension: ')
        working_img = cv.imread('C:/Users/vishn/Personal/3d_plotter/working_files/' + filename)

        detector = EdgeDetect(working_img)
        detector.adjust_image((5, 5))
        detector.find_canny_thresh()

        return detector.contours