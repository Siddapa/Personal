import socket
import pickle
import numpy as np
import cv2 as cv
from edge_detect import EdgeDetect
from plotting.plotter import Plotter
from matplotlib import pyplot as plt


class Server:
    def __init__(self) -> None:
        # Needs to self host since serving data
        self.address = '0.0.0.0'
        self.port = 65432
        self.packet_size = 4096

    """
    Waits for contour data from OpenCV
    Decodes data and stores as self.contours
    """
    def await_receive(self) -> None:
        tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Awaiting Connection...')
        tunnel.bind((self.address, self.port))
        tunnel.listen()

        conn, _ = tunnel.accept()
        data = b""
        while True:
            packet = conn.recv(self.packet_size)
            if not packet: break
            data += packet
        self.contours = pickle.loads(data)
        print('Data Received')


    """
    Runs the plotter functions to move the arm itself
    Calibration is handled manually and confirmed by the touch sensor
    """
    def draw(self) -> None:
        plotter = Plotter(self.contours)

        print('Power off the printer and set axes to endpoints')
        print()
        plotter.calibrate()

        print('Drawing Image...')
        print()
        plotter.draw_image()


    """
    Redraws the contours on a blank numpy array to ensure data
    received matche the data sent
    Purely for debuggin purposes
    """
    def display_contours(self) -> None:
        black_image = np.zeros((600, 800, 3), dtype = "uint8")
        for contour in self.contours:
            for point in contour:
                x_coord = point[0][0]
                y_coord = point[0][1]
                black_image[y_coord, x_coord] = [0, 255, 0]
        plt.imshow(black_image, interpolation='nearest')
        plt.show()
        # cv.imshow('Plot', black_image)
        # cv.waitKey(0)


    def output_coordinates(self) -> None:
        for contour in self.contours:
            for point in contour:
                print(point)
            print()


class Client:
    def __init__(self, address, port) -> None:
        # Needs to be adjustable since server ip can change based on DHCP
        self.address = address
        self.port = port

    """
    Dumps contour data over socket
    """
    def send(self) -> None:
        tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tunnel.connect((self.address, self.port))
        contours = self.detect_image()

        data = pickle.dumps(contours)
        tunnel.send(data)

    """
    Runns Canny image filter (edge detector) for specficed image
    """
    def detect_image(self):
        filename = input('Input Filename with Extension: ')
        working_img = cv.imread('C:/Users/vishn/Personal/3d_plotter/working_files/' + filename)

        detector = EdgeDetect(working_img)
        detector.adjust_image((5, 5))
        detector.find_canny_thresh()

        return detector.contours
